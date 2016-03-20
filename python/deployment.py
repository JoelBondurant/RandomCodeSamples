""" Python Common Deployment Utils Package """
import os, site

def sitepath(package = 'analyticobjects', stdout = True):
	pth = os.path.join(site.getsitepackages()[0], package)
	if stdout:
		print(pth)
	return pth

