# Migration to fix Usuario inheritance
from django.db import migrations, models
import django.db.models.deletion

def forwards_populate_users(apps, schema_editor):
    Administrador = apps.get_model('usuarios', 'Administrador')
    Propietario = apps.get_model('usuarios', 'Propietario')
    Turista = apps.get_model('usuarios', 'Turista')
    Usuario = apps.get_model('usuarios', 'Usuario')
    db_alias = schema_editor.connection.alias

    # Handle Administrador instances
    for admin in Administrador.objects.using(db_alias).all():
        usuario = Usuario.objects.using(db_alias).create(
            id=admin.id,
            nombre=admin.nombre,
            correo=admin.correo,
            contrasena=admin.contrasena,
            tipo='administrador',
            idiomaPreferido=admin.idioma_preferido
        )
        admin.usuario_ptr = usuario
        admin.save()

    # Handle Propietario instances
    for prop in Propietario.objects.using(db_alias).all():
        usuario = Usuario.objects.using(db_alias).create(
            id=prop.id,
            nombre=prop.nombre,
            correo=prop.correo,
            contrasena=prop.contrasena,
            tipo='propietario',
            idiomaPreferido=prop.idioma_preferido
        )
        prop.usuario_ptr = usuario
        prop.save()

    # Handle Turista instances
    for turista in Turista.objects.using(db_alias).all():
        usuario = Usuario.objects.using(db_alias).create(
            id=turista.id,
            nombre=turista.nombre,
            correo=turista.correo,
            contrasena=turista.contrasena,
            tipo='turista',
            idiomaPreferido=turista.idioma_preferido
        )
        turista.usuario_ptr = usuario
        turista.save()

def backwards_unpopulate(apps, schema_editor):
    # Delete Usuario instances that are linked to all child models
    Administrador = apps.get_model('usuarios', 'Administrador')
    Propietario = apps.get_model('usuarios', 'Propietario')
    Turista = apps.get_model('usuarios', 'Turista')
    Usuario = apps.get_model('usuarios', 'Usuario')
    db_alias = schema_editor.connection.alias
    
    # Get all Usuario IDs that are linked to child models
    admin_user_ids = Administrador.objects.using(db_alias).values_list('usuario_ptr_id', flat=True)
    prop_user_ids = Propietario.objects.using(db_alias).values_list('usuario_ptr_id', flat=True)
    turista_user_ids = Turista.objects.using(db_alias).values_list('usuario_ptr_id', flat=True)
    
    # Delete those Usuario instances
    Usuario.objects.using(db_alias).filter(
        id__in=list(admin_user_ids) + list(prop_user_ids) + list(turista_user_ids)
    ).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_administrador_propietario_turista_delete_usuario'),
    ]

    operations = [
        # 1. Create the Usuario model first
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('contrasena', models.CharField(max_length=255)),
                ('tipo', models.CharField(max_length=50)),
                ('idiomaPreferido', models.CharField(default='es', max_length=10)),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'db_table': 'usuarios',
            },
        ),
        
        # 2. Add usuario_ptr field (initially nullable) for all models
        migrations.AddField(
            model_name='administrador',
            name='usuario_ptr',
            field=models.OneToOneField(
                to='usuarios.Usuario',
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                parent_link=True,
                auto_created=True,
            ),
        ),
        migrations.AddField(
            model_name='propietario',
            name='usuario_ptr',
            field=models.OneToOneField(
                to='usuarios.Usuario',
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                parent_link=True,
                auto_created=True,
            ),
        ),
        migrations.AddField(
            model_name='turista',
            name='usuario_ptr',
            field=models.OneToOneField(
                to='usuarios.Usuario',
                on_delete=django.db.models.deletion.CASCADE,
                null=True,
                parent_link=True,
                auto_created=True,
            ),
        ),
        
        # 2. Populate Usuario instances and link them
        migrations.RunPython(forwards_populate_users, backwards_unpopulate),
        
        # 3. Make usuario_ptr non-nullable for all models
        migrations.AlterField(
            model_name='administrador',
            name='usuario_ptr',
            field=models.OneToOneField(
                to='usuarios.Usuario',
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                auto_created=True,
            ),
        ),
        migrations.AlterField(
            model_name='propietario',
            name='usuario_ptr',
            field=models.OneToOneField(
                to='usuarios.Usuario',
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                auto_created=True,
            ),
        ),
        migrations.AlterField(
            model_name='turista',
            name='usuario_ptr',
            field=models.OneToOneField(
                to='usuarios.Usuario',
                on_delete=django.db.models.deletion.CASCADE,
                parent_link=True,
                auto_created=True,
            ),
        ),
        
        # 4. Remove duplicate fields that are now inherited
        # For Administrador
        migrations.RemoveField(model_name='administrador', name='nombre'),
        migrations.RemoveField(model_name='administrador', name='correo'),
        migrations.RemoveField(model_name='administrador', name='contrasena'),
        migrations.RemoveField(model_name='administrador', name='tipo'),
        migrations.RemoveField(model_name='administrador', name='idioma_preferido'),
        
        # For Propietario
        migrations.RemoveField(model_name='propietario', name='nombre'),
        migrations.RemoveField(model_name='propietario', name='correo'),
        migrations.RemoveField(model_name='propietario', name='contrasena'),
        migrations.RemoveField(model_name='propietario', name='tipo'),
        migrations.RemoveField(model_name='propietario', name='idioma_preferido'),
        
        # For Turista
        migrations.RemoveField(model_name='turista', name='nombre'),
        migrations.RemoveField(model_name='turista', name='correo'),
        migrations.RemoveField(model_name='turista', name='contrasena'),
        migrations.RemoveField(model_name='turista', name='tipo'),
        migrations.RemoveField(model_name='turista', name='idioma_preferido'),
        
        # 5. Update model options for proper inheritance
        migrations.AlterModelOptions(
            name='administrador',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='propietario',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='turista',
            options={'base_manager_name': 'objects'},
        ),
    ]
    
    
