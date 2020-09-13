frappe.pages['posapp'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'POS APP',
		single_column: true
	});

	$('.page-head').remove();
	

	this.page.$table_tool = new frappe.PosApp.posapp(this.page);

	$('div.navbar-fixed-top').find('.container').css('padding', '0');
	
	$("head").append("<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css' />"); 
	$("head").append("<link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900' />"); 
	$("head").append("<link href='https://cdn.jsdelivr.net/npm/vuetify@2.x/dist/vuetify.min.css' rel='stylesheet'>"); 	
}
