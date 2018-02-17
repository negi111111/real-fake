# GANで生成した画像の評価(pix2pix ver)
## 使い方
`python app.py`
したら

>http://127.0.0.1:5000/

にアクセスして，回答．表示画像は，[pix2pix](https://arxiv.org/abs/1611.07004)と同じ回答方式にして，1秒画像表示したら消える仕様にしてある．自分の画像でやる場合は，`static/data/real/`に本物画像，`static/data/fake/`に偽物画像入れて`labels.json`に以下の感じに画像パスとラベル渡せばOK．最後に，偽物と本物の正答率の表示とどれを間違ったのか，回答結果はcsv形式でDL可．

>{
>"data/real/1.jpg": true,  
>"data/real/2.jpg": true,  
>"data/real/3.jpg": true,  
>"data/fake/48.png": false,  
>"data/fake/49.png": false,  
>"data/fake/50.png": false,  
>}
> 
![s1](https://github.com/negi111111/real-fake/blob/master/images/s1.png)
![s2](https://github.com/negi111111/real-fake/blob/master/images/s2.png)
![s3](https://github.com/negi111111/real-fake/blob/master/images/s3.png)
