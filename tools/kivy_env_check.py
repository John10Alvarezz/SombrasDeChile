import sys
import os
import pkgutil

print('Python', sys.version.replace('\n',' '))
try:
    import kivy
    print('kivy version:', kivy.__version__)
except Exception as e:
    print('kivy import error:', repr(e))

print('KIVY_GL_BACKEND =', os.environ.get('KIVY_GL_BACKEND'))
print('KIVY_WINDOW =', os.environ.get('KIVY_WINDOW'))
print('SDL_VIDEODRIVER =', os.environ.get('SDL_VIDEODRIVER'))

for pkg in ('kivy_deps.sdl2', 'kivy_deps.glew', 'kivy_deps.angle'):
    loader = pkgutil.find_loader(pkg)
    print(pkg, 'installed:', loader is not None)

# List installed packages (top 30) to help debugging
try:
    import pkg_resources
    dists = list(pkg_resources.working_set)
    dists.sort(key=lambda x: x.project_name.lower())
    print('\nInstalled packages (sample):')
    for d in dists[:60]:
        print('-', d.project_name, d.version)
except Exception as e:
    print('Could not list installed packages:', e)
