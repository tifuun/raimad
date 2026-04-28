import raimad as rai
from random import Random

class Resonator(rai.Compo):
    def _make(self, seed):
        r = Random()
        r.seed(seed)
        rng = r.random

        self.subcompos.r1 = (
            rai.RectLW(rng() * 2e6, rng() * 2e6).proxy()
            .move(rng() * 4e6, rng() * 4e6)
            )

        self.subcompos.r2 = (
            rai.RectLW(rng() * 2e6, rng() * 2e6).proxy()
            .move(rng() * 4e6, rng() * 4e6)
            )

        self.subcompos.r3 = (
            rai.RectLW(rng() * 2e6, rng() * 2e6).proxy()
            .move(rng() * 4e6, rng() * 4e6)
            )

        self.marks.mark1 = self.subcompos.r1.bbox.bot_left
        self.marks.mark2 = self.subcompos.r2.bbox.bot_left

class FooF(rai.Compo):
    def _make(self, seed):
        r = Random()
        r.seed(seed)
        rng = r.random

        final = rng()

        res_temp = Resonator(seed)
        self.subcompos.res1 = res_temp.proxy()
        res2 = (
            res_temp.proxy()
            .vflip()
            .hflip()
            .move(0, rng() * 100e6)
            .marks.mark2.to(self.subcompos.res1.marks.mark1)
            .move(0, -final * 100e6)
            )

        self.subcompos.res2 = res2

        print('\n\n\nFOOF')
        print(self.subcompos.res1.marks.mark1)
        print(self.subcompos.res1.marks.mark2)
        print(self.subcompos.res2.marks.mark1)
        print(self.subcompos.res2.marks.mark2)

class FooT(rai.Compo):
    def _make(self, seed):
        r = Random()
        r.seed(seed)
        rng = r.random

        final = rng()

        res_temp = Resonator(seed)
        self.subcompos.res1 = res_temp.proxy()
        res2 = (
            res_temp.proxy()
            .vflip()
            .hflip()
            #.move(0, rng() * 100e6)
            .marks.mark2.to(self.subcompos.res1.marks.mark1)
            .move(0, -final * 100e6)
            )

        self.subcompos.res2 = res2

        print('\n\n\nFOOt')
        print(self.subcompos.res1.marks.mark1)
        print(self.subcompos.res1.marks.mark2)
        print(self.subcompos.res2.marks.mark1)
        print(self.subcompos.res2.marks.mark2)

class Chip(rai.Compo):
    def _make(self, seed, alt):
        compo = [FooT, FooF][alt]

        self.subcompos.sub1 = compo(seed).proxy().move(1e6, 1e6)

def fuzz():
    for seed in range(1000):
        print(seed)

        c1 = rai.export_cif(Chip(seed, True))
        c2 = rai.export_cif(Chip(seed, False))

        c2r = c2.replace('FooT', 'FooF') # patch cell names to match
        assert c2 != c2r

        if c1 != c2r:
            print("FAIL!!")
            print(seed)
            break
            
    with open('c1.cif', 'w') as f:
        f.write(c1)
    with open('c2.cif', 'w') as f:
        f.write(c2r)

if __name__ == '__main__':
    fuzz()

