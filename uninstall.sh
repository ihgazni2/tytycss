#pip3 uninstall main
pip3 uninstall tytycss
git rm -r dist
git rm -r build
#git rm -r tytycss.egg-info
git rm -r tytycss.egg-info
rm -r dist
rm -r build
#rm -r tytycss.egg-info
rm -r tytycss.egg-info
git add .
git commit -m "remove old build"
