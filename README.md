# Sistema de información para servicios de alimentación
Gestión de insumos basado en la formulación de menús

### Requerimientos

- Django==1.11
- Pillow==4.1.0
- django-crispy-forms==1.6.1
- django-summernote==0.8.7
- pyexcel-xlsx==0.5.0.1
- psycopg2==2.6.2 # para  postgress

### Instalación

`git clone https://github.com/gitdealdo/serva.git`
`cd serva`
`virtualenv --python=python3 env`
`source env/bin/activate `
`pip install -r requiriements.txt`
`python manage.py migrate  --settings=config.settings.local` # local para desarrollo
`python manage.py runserver  --settings=config.settings.local`# local para desarrollo
