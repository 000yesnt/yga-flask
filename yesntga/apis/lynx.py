import os
import random
import glob
from flask import make_response
from flask_restful import Resource
from util import no_cache, mplat_file_mime

def bake(glb, int_path_name):
    r = make_response()
    i = random.randint(0, len(glb) - 1)
    return no_cache(r, {
        'X-Accel-Redirect': os.path.join(f"/int/{int_path_name}/", os.path.basename(glb[i])),
        'Lynx': os.path.basename(glb[i]),
        'Content-Type': mplat_file_mime(os.path.join(os.path.dirname(glb[0]), os.path.basename(glb[i])))
    })
# ... okay this is weird.
lynxglob = "/var/lynx/*"
lynxwebpglob = "/var/lynx/webp/*"

class Lynx(Resource):
    lynxes = [f for f in glob.glob(lynxglob) if not os.path.isdir(f)]
    def get(self):
        if not len(self.lynxes):
            return "ERR: We somehow don't have any lynxes to send :(", 500
        return bake(self.lynxes, 'lynx')

class LynxWebP(Resource):
    lynxes = [f for f in glob.glob(lynxwebpglob) if not os.path.isdir(f)]
    def get(self):
        if not len(self.lynxes):
            return "ERR: We somehow don't have any lynxes to send :(", 500
        return bake(self.lynxes, 'lynxwebp')