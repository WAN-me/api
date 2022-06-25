#!/bin/bash

send() {
    local text="${1}"
    local msg=$( phpurlencode "$text" )
    curl "https://api.telegram.org/bot$TGTOKEN/sendMessage?chat_id=$TGCHAT&parse_mode=HTML&text=$msg"
}

phpurlencode() {
  local hexchars="0123456789ABCDEF"
  local string="${1}"
  local strlen=${#string}
  local encoded=""

  for (( pos=0 ; pos<strlen ; pos++ )); do
        c=${string:$pos:1}
        if [ "$c" == ' ' ];then
                encoded+='+'
        elif ( [[ "$c" != '!' ]] && [ "$c" \< "0" ] && [[ "$c" != "-" ]] && [[ "$c" != "." ]] ) || ( [ "$c" \< 'A' ] && [ "$c" \> '9' ]  ) || ( [ "$c" \> 'Z' ] && [ "$c" \< 'a' ] && [[ "$c" != '_' ]]  ) || ( [ "$c" \> 'z' ] );then
                hc=`printf '%X' "'$c"`
                dc=`printf '%d' "'$c"`
                encoded+='%'
                f=$(( $dc >> 4 ))
                s=$(( $dc & 15 ))
                encoded+=${hexchars:$f:1}
                encoded+=${hexchars:$s:1}
        else
                encoded+=$c
        fi
  done
  echo "${encoded}"    # You can either set a return variable (FASTER) 
  REPLY="${encoded}"   #+or echo the result (EASIER)... or both... :p
}

BRANCH=$1
PORT=33030
# Pre tasks
echo "branch $BRANCH"
rm ~/test.out
# download repo
rm -rf ~/.apitemp
mkdir -p ~/.apitemp 2>> ~/test.out
cd ~/.apitemp 2>> ~/test.out

git clone git@github.com:wan-me/api.git 2>> ~/test.out

cd api 2>> ~/test.out
git checkout $BRANCH 2>> ~/test.out
fuser $PORT/tcp -k
# create cfg

cat example.cfg.py | sed "s,^api_port = .*,api_port = $PORT,g" > cfg.py 2>> ~/test.out

TGTOKEN="5213806122:AAEGsk8oKYiB9NJx_BZpJ33LkPHlG67BxLw"
TGCHAT="-650801396"


STDt=`python3 test.py $PORT 2>> ~/test.out` \
&& ( 
    echo 'test successful!' 
    send "test succesful on branch $BRANCH"
    cd ~/$BRANCH/api  2>> ~/test.out
    ( 
        STDp=`git pull 2> ~/test.out` && systemctl restart api && send "ok pull"
    ) || ( 
            ERROR="failed pull on branch $BRANCH
<code>$(cat ~/test.out)</code>
"
            send "$ERROR"
        ) && (cp text.sh ~/apitest.sh && bash update.sh) 
    ) || ( 
    echo 'Test failed' 
    send "testing fail on branch $BRANCH
<code>$(cat ~/test.out)</code>
"
    
    
    )


# post tasks

# rm temp
cd ~
rm -rf ~/.apitemp