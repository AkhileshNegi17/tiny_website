# coding: utf8
from os import path

signature = db.Table(db,'auth_signature',
      Field('created_on','datetime',default=request.now,
            writable=False,readable=False, label=T('Created on')),
        Field('created_by',auth.settings.table_user,default=auth.user_id,
            writable=False,readable=False, label=T('Created by')),
        Field('modified_on','datetime',update=request.now,default=request.now,
            writable=False,readable=False, label=T('Modified on')),
      Field('modified_by',auth.settings.table_user,
            default=auth.user_id,update=auth.user_id,
            writable=False,readable=False, label=T('Modified by'))
      )

db._common_fields.append(signature) #db._common_fields is a list of fields that should belong to all the tables

db.define_table('website_parameters',
    Field('website_name_long', label=T('Website name long')),
    Field('website_name', label=T('Website name')),
    Field('website_url', label=T('Url')),
    Field('contact_name', label=T('Contact name')),
    Field('contact_trade_register_number', label=T('Trade register number')),
    Field('contact_address', 'text', label=T('Address')),
    Field('contact_google_maps_plan_url', 'text', label=T('Google maps plan url')),
    Field('contact_telephone', label=T('Telephone')),
    Field('contact_fax', label=T('Fax')),
    Field('contact_mobile', label=T('Mobile')),
    Field('contact_form_email', label=T('Contact form email')),
    Field('contact_form_cc', label=T('Contact form cc')),
    Field('contact_form_bcc', label=T('Contact form cci')),
    Field('booking_form_email', label=T('Booking form email')),
    Field('booking_form_cc', label=T('Booking form cc')),
    Field('booking_form_bcc', label=T('Booking form cci')),
    Field('mailserver_url', label=T('Mail server url')),
    Field('mailserver_port', 'integer', label=T('Mail server port')),
    Field('mailserver_sender_mail', label=T('Mail server sender email')),
    Field('mailserver_sender_login', label=T('Mail server sender login')),
    Field('mailserver_sender_pass', label=T('Mail server sender pass')),
    Field('google_analytics_id', label=T('Google analytics id')),
    Field('banner_image_desktop', label=T('Banner image on desktop')),
    Field('banner_image_tablet', label=T('Banner image on tablet')),
    Field('banner_image_phone', label=T('Banner image on phone'))
) 
db.website_parameters.website_url.requires = IS_EMPTY_OR(IS_URL())
db.website_parameters.mailserver_sender_mail.requires = IS_EMPTY_OR(IS_URL())
db.website_parameters.contact_form_email.requires = IS_EMPTY_OR(IS_EMAIL())
db.website_parameters.contact_form_cc.requires = IS_EMPTY_OR(IS_EMAIL())
db.website_parameters.contact_form_bcc.requires = IS_EMPTY_OR(IS_EMAIL())
db.website_parameters.booking_form_email.requires = IS_EMPTY_OR(IS_EMAIL())
db.website_parameters.booking_form_cc.requires = IS_EMPTY_OR(IS_EMAIL())
db.website_parameters.booking_form_bcc.requires = IS_EMPTY_OR(IS_EMAIL())

db.define_table('page_component',
    Field('controller', readable=False, writable=False, default='default', label=T('Component controller')),
    Field('name', readable=False, writable=False, label=T('Component name')),
    Field('ajax', 'boolean', readable=False, writable=False, default=False, label=T('Component with Ajax')),
    Field('ajax_trap', 'boolean', readable=False, writable=False, default=False, label=T('Component with Ajax trap'))
)

db.define_table('page',
    Field('parent', 'reference page', label=T('Parent')),
    Field('title', unique=True, notnull=True, label=T('Title')),
    Field('rank', 'integer', readable=False, writable=False, default=0, label=T('Rank')),
    Field('subtitle', label=T('Subtitle')),
    Field('url', unique=True, readable=False, writable=False, label=T('Url')),
    Field('content', 'text', label=T('Content')),
    Field('is_index', 'boolean', readable=False, writable=False, label=T('Is index')),
    Field('is_enabled', 'boolean', readable=False, writable=False, default=True, label=T('Is enabled')),
    Field('left_sidebar_enabled', 'boolean', default=False, label=T('Left sidebar')),
    Field('right_sidebar_enabled', 'boolean', default=True, label=T('Right sidebar')),
    Field('left_sidebar_component', 'reference page_component', label=T('Left sidebar component')),
    Field('right_sidebar_component', 'reference page_component', label=T('Right sidebar component')),
    format='%(title)s'
)
db.page.parent.requires = IS_EMPTY_OR(IS_IN_DB(db, db.page.id, '%(title)s', zero=T('<Empty>')))
db.page.left_sidebar_component.requires = IS_EMPTY_OR(IS_IN_DB(db, db.page_component.id, '%(name)s', zero=T('<Empty>')))
db.page.right_sidebar_component.requires = IS_EMPTY_OR(IS_IN_DB(db, db.page_component.id, '%(name)s', zero=T('<Empty>')))
db.page.url.compute = lambda row: IS_SLUG()(row.title)[0]

db.define_table('image',
    Field('name', notnull=True, label=T('Name')),
    Field('alt', label=T('Alt')),
    Field('comment', label=T('Comment')),
    Field('file', 'upload', uploadfolder=path.join(
        request.folder,'static','images','photo_gallery'
        ), autodelete=True, label=T('File')),
    Field('thumb', 'text', readable=False, writable=False, label=T('Thumb')),
    Field('show_in_gallery', 'boolean', readable=False, writable=False, default=True, label=T('Show in gallery')),
    Field('show_in_banner', 'boolean', readable=False, writable=False, default=False, label=T('Show in banner')),
    format='%(name)s'
)
db.image.alt.compute = lambda row: row.name.capitalize()

db.define_table('registered_user',
    Field('first_name', label=T('First name')),
    Field('last_name', label=T('Last name')),
    Field('email', unique=True, requires=[IS_EMAIL(), IS_NOT_IN_DB(db, 'registered_user.email')], label=T('Email')),
    format='%(email)s'
    )

db.define_table('news',
   Field('title', label=T('Title')),
   Field('date','date',default=request.now,label=T('Date')),
   Field('text','text',label=T('News content')),
   Field('published_on', 'datetime', default=request.now),
   format='%(text)s'
   )

db.define_table('file',
   Field('title', label=T('Title'), notnull=True),
   Field('comment', label=T('Comment')),
   Field('file', 'upload', uploadfolder=path.join(
        request.folder,'static','uploaded_files'
        ), notnull=True, autodelete=True, label=T('File')),
   Field('size', 'double', readable=False, writable=False, label=T('Size')),
   format='%(title)s'
   )
db.file.size.compute = lambda row: path.getsize(path.join(request.folder,'static','uploaded_files',row.file))

## after defining tables, uncomment below to enable auditing
auth.enable_record_versioning(db)


