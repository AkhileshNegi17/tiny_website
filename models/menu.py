# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

## read more at http://dev.w3.org/html5/markup/meta.name.html
# response.meta.author = 'Your Name <you@example.com>'
# response.meta.description = 'a cool new app'
# response.meta.keywords = 'web2py, python, framework'
# response.meta.generator = 'Web2py Web Framework'

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################


if WEBSITE_PARAMETERS:
	#If we don't show the banner, we add the website name with a link to index page
	if not WEBSITE_PARAMETERS.with_banner:
		website_name=[XML(c) if c.islower() else B(c) for c in WEBSITE_PARAMETERS.website_name]
		response.logo = A(website_name,_class="brand",_href=URL('default','index'))
	if WEBSITE_PARAMETERS.website_title:
		response.title = WEBSITE_PARAMETERS.website_title
	if WEBSITE_PARAMETERS.website_subtitle:
		response.subtitle = WEBSITE_PARAMETERS.website_subtitle



pages = db(db.page.is_index==False).select(orderby=db.page.rank|db.page.title)

for p in pages:
	child_pages = db(db.page.parent==p.id).select(orderby=db.page.rank|db.page.title,)
	if child_pages:
		child_list = []
		for c in child_pages:
			child_list.append([c.title, False, URL('pages','show_page', args=c.url)])
		response.menu += [(p.title, False, URL('default','index'), child_list)]
	else:
		if not p.parent:
			response.menu += [(p.title, False, URL('pages','show_page', args=p.url))]

images = db(db.image).select()
if images:
	response.menu += [(T('Photo gallery'), False, URL('images','images'))]

files = db(db.file.page==None).select()
if files or auth.has_membership('manager'):
	response.menu += [(T('Files to download'), False, URL('files','files_list'))]

if auth.has_membership('booking_manager'):
	response.menu += [(T('Booking requests'), False, URL('calendar','edit_booking_requests'))]
response.menu += [(T('Contact us'), False, URL('default','contact_form'))]

# if auth.has_membership('manager'):
# 	response.menu += [(T('Website administration'),False, None, [
# 			[T('Add a page'), False, URL('default', 'edit_page')],
# 			[T('Add an image in library'), False, URL('images', 'edit_image')],
# 		])]

#Disable "registration" and "lost password" menu
auth.settings.actions_disabled.append('register') 
auth.settings.actions_disabled.append('request_reset_password')
