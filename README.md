# logos_cafesystem

工大祭で利用するための注文システムです。

```
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata fixture/item.json
python manage.py loaddata fixture/detail.json
python manage.py runserver
```

作成にあたっては以下のリポジトリを参考にしました。
[epicserve:Django Inline Formset Example]
https://github.com/epicserve/inlineformset-example
