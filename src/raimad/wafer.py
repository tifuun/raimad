#!/usr/bin/env python
# coding: utf-8

# In[3]:


import raimad as rai
import numpy as np

class Wafer(rai.Compo):
    def _make(self, diameter: float = 100e2, flats: list = [32.5e2], flat_angle: list = [0]):
        '''
        This class provides a wafer as a base. The wafer is centred around 0,0. 
        One can provide the lenght of each flat as well as theirs corresponding angles (w.r.t. the bottom) as a list 

        The standard diameter is 100 mm (1e5 um)
        The standard flat is 32.5 mm at the bottom
        '''
        
        Contour = rai.Circle(radius = diameter/2)
        for i, flat in enumerate(flats):
            # Extract the points of the contour (ensure this is a reference and not a copy)
            points = Contour.geoms['root'][0]
        
            # Calculate the cut distance and direction of the flats
            cut_distance = np.sin(np.arccos(flats[i]/diameter)) * diameter / 2
            cut_point = (cut_distance*np.cos(flat_angle[i]).item(),
                         cut_distance*np.sin(flat_angle[i]).item()
                        )
            
            # Identify points to be removed
            j_store = []
            for j, point in enumerate(points):
                if np.linalg.norm(np.subtract(point, cut_point)) < flats[i]/2: #Constraints for points outside of flat
                    j_store.append(j)
            
            # Add corner points at the correct position
            points[j_store[0]] = (cut_distance*np.cos(flat_angle[i])-np.sin(flat_angle[i])*-flats[i]/2,
                                  cut_distance*np.sin(flat_angle[i])+np.cos(flat_angle[i])*-flats[i]/2)
            points[j_store[-1]] = (cut_distance*np.cos(flat_angle[i])-np.sin(flat_angle[i])*flats[i]/2,
                                  cut_distance*np.sin(flat_angle[i])+np.cos(flat_angle[i])*flats[i]/2)

            if 0 in j_store:
                points[j_store[0]] ,points[j_store[-1]] = points[j_store[-1]], points[j_store[0]]
    
            j_store = j_store[1:-1]
            
            # Remove elements by index in reverse order
            for index in sorted(j_store, reverse=True):
                    del points[index]
            
            self.subcompos.Wafer = Contour.proxy().rotate(np.deg2rad(-90)).map('_wafer_contour')


# In[5]:


Wafer().proxy().scale(1e-2)


# In[ ]:




