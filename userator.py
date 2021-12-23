MESAJ="U S Σ R Δ T O R / S T R İ N G 💣"
MESAJ+="\nTelegram: @UseratorOT"
pkg upgrade
clear
echo -e $MESAJ
echo "Python yüklənir..."
pkg install python -y
clear
echo -e $MESAJ
echo "TeleThon yüklənir..."
pip install telethon
echo "Requests/BS4 yüklənir..."
pip install requests
pip install bs4
clear
echo -e $MESAJ
echo "Fayl yazılır..."
curl "https://raw.githubusercontent.com/Goqerti/userator/master/userator.py" --output "userator.py"
clear
echo -e $MESAJ
echo "Qurulum Bitdi! İndi String Ala Bilərsiz."
clear
python userator.py
