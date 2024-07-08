# Arkana Training
Arkana Training - Internal

## CARA MEMBUAT NEW MODULE ODOO ARKANA_BASE_TRAINING (UBUNTU)

Setelah Odoo dan database odoo16_arkana_training berjalan dengan baik, maka untuk memulainya kita harus membuat sebuah modul baru. Odoo telah menyiapkan fitur yang bernama SCAFFOLD, yang berfungsi untuk membuat template modul secara instan yang mengandung komponen default pada sebuah modul Odoo.

1. Pertama-tama, Buat Folder modul baru bernama arkana_base_training :
Buka terminal dan navigasikan ke direktori yang sebelumnya kita telah buat. Lalu, buat folder projectnya dengan perintah:
```bash
cd
# membuat folder modul
mkdir arkana_base_data

```

2. Selanjutnya Instal Scaffold.
Untuk membuat kerangka kerja pada modul yang telah kita buat sebelumnya, maka di perlukan inisialisasi menggunakan scaffold dengan perintah berikut :

```bash
#Inisialisasi Scaffold
scaffold init arkana_base_data
```
Setelah kita mengeksekusi perintah di atas, maka pada folder project arkana_base_data kita akan tercipta sebuah modul baru dengan struktur sebagai berikut :
```bash
arkana_base_data
…. controllers
……… __init__.py
……… controllers.py
…. demo
……… demo.xml
…. models
……… __init__.py
……… models.py
…. security
……… ir.model.access.csv
…. views
……… templates.xml
……… views.xml
…. __init__.py
…. __manifest__.py
```
Pada hirarki diatas, maka struktur MVC (Model View Controller) sudah terbentuk dengan adanya pembagian hirarki berdasarkan folder.

3. Setelah itu konfigurasi file (__manifest__.py) sesuai dengan kebutuhan:

```bash
# Install
# -*- coding: utf-8 -*-
{
    'name': "training_odoo",
 
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
 
    'description': """
        Long description of module's purpose
    """,
 
    'author': "My Company",
    'website': "https://www.yourcompany.com",
 
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
 
    # any module necessary for this one to work correctly
    'depends': ['base'],
 
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

```

5. Setelah kita mengupdate informasi di file __manifest__, maka kita lanjutkan dengan proses instalasi modul project kita di menu Apps, yaitu klik menu Apps > Update Apps List. Untuk melihat menu Update Apps List, maka kita harus mengaktifkan Developer Mode, caranya masuk ke menu Setting lalu scroll paling bawah dan klik sebuah link ‘Activate the developer mode’. Selanjutnya kita kembali ke menu Apps > Update Apps List dan cari modul sesuai nama modul training kita yaitu ‘arkana_base_training’.
