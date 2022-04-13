#!/bin/bash
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


$STD=python3 test.py $PORT 2> testes.txt \
&& ( 
    echo 'test successful!' 
    curl "https://api.telegram.org/bot$TGTOKEN/sendMessage?chat_id=$TGCHAT&text=test+succesful+on+branch+$BRANCH"
    cd ~/$BRANCH/api
    ( git pull && curl "https://api.telegram.org/bot$TGTOKEN/sendMessage?chat_id=$TGCHAT&text=test+ok+pull"
    ) || ( curl "https://api.telegram.org/bot$TGTOKEN/sendMessage?chat_id=$TGCHAT&text=failed+pull" ) 
    ) || ( 
    echo 'Test failed' 
    TEXT="testing fail on branch $BRANCH\n<code>$STD</code>"
    MSG=$( phpurlencode "$TEXT" )
    curl "https://api.telegram.org/bot$TGTOKEN/sendMessage?chat_id=$TGCHAT&parse_mode=HTML&text=$MSG"
    
    )


# post tasks

# rm temp
cd ~
rm -rf ~/.apitemp

