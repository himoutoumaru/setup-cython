import os
import platform
import shutil
from distutils.command.build_ext import build_ext
from glob import glob
from pathlib import Path
from Cython.Build import cythonize
from setuptools import setup, Extension, find_packages

local_packages = find_packages()

# local_packages.remove('tests')

bin_script = '{{cookiecutter.bootstrap_name}}'
mod = '{{cookiecutter.package_name}}'

with_scikit = '{{cookiecutter.use_scikit}}'
with_statics_model = '{{cookiecutter.use_statics_model}}'

extentions = []
for obj in local_packages:
    dir_path = os.path.join('.', obj.replace(".", "/"))
    for name in os.listdir(dir_path):
        if "__" in name or os.path.isdir(dir_path + "/" + name):
            continue
        extentions.append(Extension(
            obj + '.' + name.replace('.py', ''), ["%s/%s" % (obj.replace(".", "/"), name)]))


class KitBuildExt(build_ext):
    def run(self):
        build_ext.run(self)

        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent

        target_dir = build_dir if not self.inplace else root_dir

        """
        把__init__.py拷贝到cython的编译目录，cython会编译不过这种脚本
        """
        for obj in local_packages:
            dir_path = obj.replace(".", "/")
            self.copy_file(Path(dir_path) / "__init__.py",
                           root_dir, target_dir)

        """
        移除Python源码
        """
        for obj in local_packages:
            for name in os.listdir(os.path.join(target_dir, obj.replace(".", "/"))):
                if "__" not in name and name.endswith(".py"):
                    os.remove(os.path.join(
                        target_dir, obj.replace(".", "/"), name))

        """
        恢复项目的层级关系，不然自身依赖会找不到的
        """
        for obj in local_packages:
            if "." not in obj:
                os.mkdir(os.path.join(target_dir, obj + "_bak"))
                shutil.move(
                    os.path.join(target_dir, obj),
                    os.path.join(target_dir, obj + "_bak"),
                )
                shutil.move(
                    os.path.join(target_dir, obj + "_bak"),
                    os.path.join(target_dir, obj),
                )

        """
        使用PyInstaller编译应用
        """
        pyinstall_spec = 'pyi-makespec ./%s.py ' % bin_script
        if with_scikit == 'yes':
            pyinstall_spec += '--hiddenimport sklearn '
            pyinstall_spec += '--hiddenimport sklearn.ensemble '
            pyinstall_spec += '--hiddenimport sklearn.tree._utils '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.typedefs '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.ball_tree '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.dist_metrics '
            pyinstall_spec += '--hiddenimport sklearn.neighbors.quad_tree '
            pyinstall_spec += '--hiddenimport sklearn.utils._cython_blas '
            pyinstall_spec += '--hiddenimport scipy._lib.messagestream '
        if with_statics_model == 'yes':
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters._conventional '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters._univariate '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._filters._inversions '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._conventional '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._univariate '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._inversions '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._classical '
            pyinstall_spec += '--hiddenimport statsmodels.tsa.statespace._smoothers._alternative '
        os.system(pyinstall_spec)

        with open('./%s.spec' % bin_script, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write('import sys\nsys.setrecursionlimit(5000)\n' + content)

        os.system('pyinstaller --clean ./%s.spec' % bin_script)
        shutil.move(os.path.join(target_dir, mod), './dist/main')

        sysstr = platform.system()
        if sysstr == "Linux":
            os.system(
                'staticx -l %s %s %s' % (
                    os.path.join(os.path.abspath('.'),
                                 'dist', bin_script + '/'),
                    './dist/%s/%s' % (bin_script, bin_script), './' + bin_script))

    def copy_file(self, path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return

        shutil.copyfile(str(source_dir / path), str(destination_dir / path))


setup(
    name=mod,
    version="0.0.4",
    description="Cython Project",
    long_description="Cython Project",
    url="",
    author="umaru",
    author_email="15875339926@139.com",
    license="MIT",
    install_requires=["cython", "logzero", "PyInstaller", "click"],
    packages=local_packages,
    platforms="any",
    entry_points={},
    zip_safe=False,
    ext_modules=cythonize(
        extentions,
        build_dir="build",
        annotate=False,
        compiler_directives=dict(always_allow_keywords=True),
        language_level=3,
    ),
    cmdclass=dict(build_ext=KitBuildExt),
)
