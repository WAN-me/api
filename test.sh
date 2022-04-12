
BRANCH=$1
PORT=33030
# Pre tasks
echo "branch $BRANCH"
# download repo
mkdir ~/.apitemp
cd ~/.apitemp

git clone https://github.com/WAN-me/api

cd api
git checkout $BRANCH
fuser $PORT/tcp -k
# create cfg

cat example.cfg.py | sed "s,^api_port = .*,api_port = $PORT,g" > cfg.py

TGTOKEN="TG TOKEN"
TGCHAT="TG CHAT"


python3 test.py $PORT 1> /dev/null \
&& ( 
    echo 'test successful!' 
    curl "https://api.telegram.org/bot$TGTOKEN/sendMessage?chat_id=$TGCHAT&text=test+succesful+on+branch+$BRANCH"
    ) || ( 
    echo 'Test failed' 
    curl "https://api.telegram.org/bot$TGTOKEN/sendMessage?chat_id=$TGCHAT&text=test+fail+on+branch+$BRANCH"
    
    )


# post tasks

# rm temp
cd ~
rm -rf ~/.apitemp

