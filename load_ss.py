import io
from PIL import Image
from cairosvg import svg2png
from scope_sheet import ExteriorScopeSheet, handwrite



scope_sheet = ExteriorScopeSheet()
scope_sheet.VALUES['gutters1']['value'] = '5" (100)'
scope_sheet.VALUES['gutters2']['value'] = '500 lf'
scope_sheet.finalize()
scope_sheet.scope_sheet.save('img/scope_sheet.png')




