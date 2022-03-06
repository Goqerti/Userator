MESAJ="U S Σ R Δ T O R ✨"
pkg update -y && pkg upgrade
clear
echo -e $MESAJ
echo "Python ✅"
pkg install python3
pip3 install --upgrade pip
clear
echo -e $MESAJ
echo "Git ✅"
pkg install git -y
clear
echo -e $MESAJ
echo "TeleThon ✅"
pip install telethon
echo "Repo ✅"
git clone https://github.com/uumud/Qurulum
clear
echo -e $MESAJ
cd Qurulum
clear
echo "U S Σ R Δ T O R ✨"
echo -e $MESAJ
pip install wheel
pip install -r requirements.txt
python3 -m up_qurulum
