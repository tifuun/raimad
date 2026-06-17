#!/usr/bin/env python3

import urllib
import re
import json
import datetime
import pickle
import socket
import struct
import time
import marionette_driver
import os
#from ipdb import pm
from IPython import embed
from pathlib import Path

#class Marionette():
#    def open(self, sock):
#        self.sock = sock
#        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        #self.sock.connect(('127.0.0.1', 2828))
#        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
#        self.sock.connect(sock)
#        self.msg_id = 1
#
#    def send_msg(self, command, params=None):
#        data = [0, self.msg_id, command, params or {}]
#        json_str = json.dumps(data)
#        prefix = f"{len(json_str)}:"
#        self.sock.sendall(prefix.encode() + json_str.encode())
#        self.msg_id += 1
#        print(f'marionette send: {json_str}')
#
#    def recv_msg(self):
#        prefix = b''
#        while b':' not in prefix:
#            prefix += self.sock.recv(1)
#        length_str = prefix[:-1].decode()
#        length = int(length_str)
#        data = self.sock.recv(length).decode()
#        loaded = json.loads(data)
#        print(f'marionette recv: {loaded}')
#        return loaded
#    
#    def new_session(self):
#        self.send_msg("session")
#        resp = self.recv_msg()
#        session_id = resp[3]['sessionId']
#        self.session_id = session_id
#
#    def url(self, url):
#        self.send_msg("url", {"url": url})
#        resp = self.recv_msg()
#
#    def get_page_source(self):
#        self.send_msg("getPageSource")
#        resp = self.recv_msg()
#        html = resp[3]
#        return html

#msg_id = 1
#
## 1. newSession (creates session)
#send_msg(sock, msg_id, "newSession")
#resp = recv_msg(sock)
#session_id = resp[3]['sessionId']
#print(f"Session ID: {session_id}") [web:21][page:1]
#
#msg_id += 1
#
## 2. Navigate to URL
#send_msg(sock, msg_id, "url", {"url": "https://example.com"})
#resp = recv_msg(sock)
#print("Navigation complete") [web:38][page:1]
#
#msg_id += 1
#
## 3. Get full page source (HTML)
#send_msg(sock, msg_id, "getPageSource")
#resp = recv_msg(sock)
#html = resp[3]
#print("Full HTML:")
#print(html[:500] + "..." if len(html) > 500 else html) [web:38][page:1]
#
## Cleanup
#msg_id += 1
#send_msg(sock, msg_id, "deleteSession")
#sock.close()
#print("Session closed") [page:1]

class Notebook():

    _pkldir = Path('archive/find-reviewers/pkl')

    def configure(self):

        self.ghapi = "https://api.github.com"

        #self.repos = [
        #    "openscad/openscad",
        #    "LibreCAD/LibreCAD",
        #    "FreeCAD/FreeCAD",
        #    "KoStard/ForgeCAD",
        #    "CadQuery/cadquery",
        #    "solvespace/solvespace",
        #    "dune3d/dune3d",
        #    "xibyte/jsketcher",
        #    "CadQuery/CQ-editor",
        #    "OpenVSP/OpenVSP",
        #    "xiangechen/chili3d",
        #    "atopile/atopile",
        #    "Adam-CAD/CADAM",
        #    "leozide/leocad",
        #    "LibrePCB/LibrePCB",
        #    "KiCad/kicad-source-mirror",
        #    "Open-Cascade-SAS/OCCT",
        #    "mlt131220/Astral3D",
        #    "gumyr/build123d"
        #    #"openjournals/joss-reviews",
        #    ]

        self.joss_repo = "openjournals/joss-reviews"

    def _save(self):
        # marionette connection cannot be pickled
        # (probably for the better)
        if hasattr(self, 'm'):
            del self.m

        self._pkldir.mkdir(exist_ok=True, parents=True)
        pklfile = self._pkldir / f"{datetime.datetime.now().isoformat()}.pkl"
        with pklfile.open('wb') as pklfd:
            pickle.dump(self, pklfd)
        print(f'wrote {pklfile}')

    @classmethod
    def _load(cls):
        pklfiles = list(sorted(cls._pkldir.glob('*.pkl'), reverse=True))
        if len(pklfiles) <= 0:
            print('no saves')
            return cls()

        pklfile = pklfiles[0]

        with pklfile.open('rb') as pklfd:
            obj = pickle.load(pklfd)

        print(f"loaded {pklfile}")

        return obj

    def _field(self, name, default):
        if not hasattr(self, name):
            setattr(self, name, default)

    def _urlget(self, url):

        if not hasattr(self, 'urlcache'):
            self.urlcache = {}

        if url in self.urlcache.keys():
            print(f'cached: {url}')

        else:
            print(f'fetch: {url}')

            req = urllib.request.Request(
                    url,
                    #headers={
                    #    'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0"
                    #    },
                    )
            resp = urllib.request.urlopen(req)
            self.urlcache[url] = resp.read()

        return self.urlcache[url]


    def _ghurlget(self, url):

        if not hasattr(self, 'urlcache'):
            self.urlcache = {}

        if url in self.urlcache.keys():
            print(f'cached: {url}')

        else:
            print(f'fetch: {url}')

            headers = {}
            #if token := os.env.get('GITHUB_API_TOKEN'):
            global token
            if globals().get('token'):
                print('token found!')
                headers['Authorization'] = f'token {token}'

            req = urllib.request.Request(
                    url,
                    headers=headers,
                    )
            resp = urllib.request.urlopen(req)
            self.urlcache[url] = resp.read()

        return self.urlcache[url]


    def get_contribs(self):

        if not hasattr(self, 'users'):
            self.users = {}

        for repo in self.relevant_repos:
            resp = self._ghurlget(f'{self.ghapi}/repos/{repo}/contributors')
            self.users[repo] = json.loads(resp)

    def compute_repos_by_users(self):
        if not hasattr(self, 'repos_by_users'):
            self.repos_by_users = {}

        for repo, users in self.users.items():
            for user in users:
                login = user['login']
                if login not in self.repos_by_users.keys():
                    self.repos_by_users[login] = set()

                self.repos_by_users[login].add(repo)


        print(f"Total unique users: {len(self.repos_by_users)}")
        print(f"Multiples:")
        for k, v in self.repos_by_users.items():
            if len(v) > 1:
                print(f"{k}: {v}")
        print()

    def get_joss_assignees(self):
        """old attempt to scrape reviewers from gh assignees -- doesnt work!"""
        #self._field('joss_issues', {})
        self._field('joss_assignees', set())

        self.joss_issues = json.loads(self._ghurlget(
            f"{self.ghapi}/repos/{self.joss_repo}/issues"
            ))

        #global issues
        #issues = self.joss_issues

        for issue in self.joss_issues:
            for assignee in issue['assignees']:
                self.joss_assignees.add(assignee['login'])

        print(f"found {len(self.joss_assignees)} joss assignees.")

    def connect_browser(self):
        self.m = marionette_driver.marionette.Marionette(
            host='127.0.0.1',
            #host='host.docker.internal',
            port=2828,
            #app=None,
            #bin=None,
            #baseurl=None,
            #socket_timeout=None,
            #startup_timeout=None,
            #**instance_args
            )
        #self.m = Marionette()
        #self.m.open('marionette.sock')
        print('created object...')
        self.m.start_session()
        print('started session...')

    def get_joss_html_pages(self):
        revpage = "https://reviewers.joss.theoj.org/reviewers"

        self._field('joss_html_pages', {})

        global html

        for page in range(0, 99999):
            self.m.navigate(f"{revpage}?page={page}")
            html = self.m.page_source
            assert 'Topic areas' in html
            self.joss_html_pages[page] = html
            #return
            #del self.urlcache[f"{revpage}?page={page}"]
            #html = self._urlget(f"{revpage}?page={page}")
            #print(len(html))
            #return

    def get_joss_reviewers(self):
        self._field('joss_reviewers', set())
        for page, html in self.joss_html_pages.items():
            matches = re.findall(r'@(\S*)</a></td>', html)
            assert len(matches) > 9
            self.joss_reviewers.update(matches)
        print(f"found {len(self.joss_reviewers)} reviewers")

    def get_interested_reviewers(self):
        #cad_contributors = set(map(str.lower, self.repos_by_users.keys()))
        #joss_reviewers = set(map(str.lower, self.joss_reviewers))
        cad_contributors = set(self.repos_by_users.keys())
        joss_reviewers = set(self.joss_reviewers)

        interested = cad_contributors.intersection(joss_reviewers)
        #print('\n'.join(interested))

        print("Potential reviewers: ")
        for name in interested:
            print(f"{name}: {' '.join(self.repos_by_users[name])}")
        print()

    def search_relevant_repos(self):
        queries = """
CAD parametric astronomy coordinate design
"""
        #global resp
        self._field('relevant_repos', set())
        for query in re.findall(r"\w+", queries):
            resp = self._ghurlget(f'{self.ghapi}/search/repositories?q={query}')
            resp = json.loads(resp)
            for result in resp['items']:
                user = result['owner']['login']
                repo = result['name']
                self.relevant_repos.add(f"{user}/{repo}")

        assert "openscad/openscad" in self.relevant_repos
        assert "LibreCAD/LibreCAD" in self.relevant_repos
        assert "FreeCAD/FreeCAD" in self.relevant_repos
        assert "CadQuery/cadquery" in self.relevant_repos

        print()
        print(f'found {len(self.relevant_repos)} relevant repos')
        print()



if 'nb' not in dir():
    nb = Notebook()._load()
nb.__class__ = Notebook

#if 'm' in dir(nb):
#    nb.m.__class__ = Marionette

nb.configure()
nb.search_relevant_repos()
nb.get_contribs()
nb.compute_repos_by_users()
nb.get_interested_reviewers()




