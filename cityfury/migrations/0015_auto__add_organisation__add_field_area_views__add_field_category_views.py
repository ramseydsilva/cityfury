# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organisation'
        db.create_table(u'cityfury_organisation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'cityfury', ['Organisation'])

        # Adding field 'Area.views'
        db.add_column(u'cityfury_area', 'views',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Category.views'
        db.add_column(u'cityfury_category', 'views',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Post.type'
        db.add_column(u'cityfury_post', 'type',
                      self.gf('django.db.models.fields.CharField')(default='I', max_length=10),
                      keep_default=False)

        # Adding field 'Post.organisation'
        db.add_column(u'cityfury_post', 'organisation',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cityfury.Organisation'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Post.views'
        db.add_column(u'cityfury_post', 'views',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Post.popularity'
        db.add_column(u'cityfury_post', 'popularity',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


        # Changing field 'Post.image'
        db.alter_column(u'cityfury_post', 'image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=100, null=True))
        # Adding field 'City.views'
        db.add_column(u'cityfury_city', 'views',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Organisation'
        db.delete_table(u'cityfury_organisation')

        # Deleting field 'Area.views'
        db.delete_column(u'cityfury_area', 'views')

        # Deleting field 'Category.views'
        db.delete_column(u'cityfury_category', 'views')

        # Deleting field 'Post.type'
        db.delete_column(u'cityfury_post', 'type')

        # Deleting field 'Post.organisation'
        db.delete_column(u'cityfury_post', 'organisation_id')

        # Deleting field 'Post.views'
        db.delete_column(u'cityfury_post', 'views')

        # Deleting field 'Post.popularity'
        db.delete_column(u'cityfury_post', 'popularity')


        # Changing field 'Post.image'
        db.alter_column(u'cityfury_post', 'image', self.gf('sorl.thumbnail.fields.ImageField')(default='', max_length=100))
        # Deleting field 'City.views'
        db.delete_column(u'cityfury_city', 'views')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'cityfury.area': {
            'Meta': {'object_name': 'Area'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'cityfury.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'cityfury.city': {
            'Meta': {'object_name': 'City'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.Country']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'publish': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'cityfury.comment': {
            'Meta': {'ordering': "('-created_date',)", 'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'cityfury.commentdislike': {
            'Meta': {'object_name': 'CommentDisLike'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.Comment']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cityfury.commentlike': {
            'Meta': {'object_name': 'CommentLike'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.Comment']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cityfury.country': {
            'Meta': {'object_name': 'Country'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'cityfury.dislike': {
            'Meta': {'unique_together': "(('user', 'post'),)", 'object_name': 'DisLike'},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cityfury.location': {
            'Meta': {'object_name': 'Location'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.City']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'string': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'cityfury.organisation': {
            'Meta': {'object_name': 'Organisation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'cityfury.post': {
            'Meta': {'ordering': "('-uploaded_date',)", 'object_name': 'Post'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.Area']", 'null': 'True', 'blank': 'True'}),
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.Category']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.City']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'dislikes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'disliked_posts'", 'symmetrical': 'False', 'through': u"orm['cityfury.DisLike']", 'to': u"orm['auth.User']"}),
            'flags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'flagged_posts'", 'symmetrical': 'False', 'through': u"orm['cityfury.PostFlag']", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.Location']", 'null': 'True', 'blank': 'True'}),
            'location_string': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'organisation': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.Organisation']", 'null': 'True', 'blank': 'True'}),
            'popularity': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['cityfury.Tag']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '10'}),
            'uploaded_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'cityfury.postflag': {
            'Meta': {'object_name': 'PostFlag'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['cityfury.Post']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'cityfury.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cityfury']