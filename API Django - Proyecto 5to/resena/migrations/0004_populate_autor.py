from django.db import migrations


def forwards_populate_autor(apps, schema_editor):
    Resena = apps.get_model('resena', 'Resena')
    Usuario = apps.get_model('usuarios', 'Usuario')
    db_alias = schema_editor.connection.alias

    for r in Resena.objects.using(db_alias).filter(autor__isnull=True):
        nombre = None
        if getattr(r, 'usuario_id', None):
            try:
                usuario = Usuario.objects.using(db_alias).get(pk=r.usuario_id)
                nombre = getattr(usuario, 'nombre', None)
            except Exception:
                nombre = None
        r.autor = nombre or 'Anónimo'
        r.save()


def backwards_unpopulate_autor(apps, schema_editor):
    # No revert: leave values as-is
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('resena', '0003_resena_autor'),
    ]

    operations = [
        migrations.RunPython(forwards_populate_autor, backwards_unpopulate_autor),
    ]
