
BRANCH=$1
# Pre tasks
echo "branch $BRANCH"
# download repo
mkdir ~/.apitemp
cd ~/.apitemp

git clone https://github.com/WAN-me/api

cd api
git checkout $BRANCH
# create cfg

cp example.cfg.py cfg.py

python3 test.py 1> /dev/null \
&& ( 
    echo 'test successful!' 
    ) || ( 
    echo 'Test failed' 
    )


# post tasks

# rm temp
cd ~
rm -rf ~/.apitemp