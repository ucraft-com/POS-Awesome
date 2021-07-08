{% include "posawesome/posawesome/page/posapp/onscan.js" %}
frappe.pages['posapp'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'POS Awesome',
		single_column: true
	});

	this.page.$PosApp = new frappe.PosApp.posapp(this.page);
	console.info('Page ');
	
	$('div.navbar-fixed-top').find('.container').css('padding', '0');
	
	$("head").append("<link href='/assets/posawesome/node_modules/vuetify/dist/vuetify.min.css' rel='stylesheet'>"); 	
	$("head").append("<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css' />"); 
	$("head").append("<link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900' />"); 
}

$.extend(
	frappe._messages, {
		"Type": "Tipo", 
		"is Offer": "é Oferta", 
		"Total Qty": "Qtd Total",
		"Customer": "Cliente",
		"Items Group": "Grupo de Itens",
		"Search Items": "Procurar Itens",
		"Additional Discount": "Desconto Adicional",
		"Items Discounts": "Descontos de Itens",
		"HOLD": "EM PAUSA",
		"Hold": "Em Pausa",
		"RETURN": "DEVOLUÇÃO",
		"Return": "Devolução",
		"CANCEL": "CANCELAR",
		"NEW": "NOVO",
		"PAY": "PAGAR",
		"Order": "Ordem",
		"Available QTY": "QTD Disponivel",
		"QTY": "QTD",
		"Discount Percentage": "Percentagem de Desconto",
		"Price list Rate": "Taxa de Lista de Preço",
		"Group": "Grupo",
		"Stock QTY": "QTD de Stock",
		"Stock UOM": "UDM de Stock",
		"Card" : "Cartão",
		"Offers" : "Ofertas",
		"Applied" : "Aplicadas",
		"There is no Customer !": "Não tem Cliente !",
		"There is no Items !" : "Não tem Itens !",
		"The existing quantity of item ${item.item_name} is not enough" : "A quantidade existente do item ${item.item_name} não é suficiente",
		"Maximum discount for Item ${item.item_name} is ${item.max_discount}%" : "Desconto Maximo para o Item ${item.item_name} é ${item.max_discount}%",
		"Selcted serial numbers of item ${item.item_name} is incorrect" : "Numeros de serie selecionado do item ${item.item_name} é incorrecto",
		"The existing batch quantity of item ${item.item_name} is not enough" : "A quantidade existente do lote para o item ${item.item_name} não é suficiente",
		"The discount should not be higher than ${this.pos_profile.posa_max_discount_allowed}%" : "O desconto não deve ser maior que ${this.pos_profile.posa_max_discount_allowed}%",
		"Return Invoice Total Not Correct" : "Total da Devolução da Factura não está Correcto",
		"Return Invoice Total should not be higher than ${this.return_doc.total}" : "Total da Devolução da Factura não deve maior que ${this.return_doc.total}",
		"The item ${item.item_name} cannot be returned because it is not in the invoice ${this.return_doc.name}" : "O item ${item.item_name} não pode ser devolvido porque não está na factura ${this.return_doc.name}",
		"The QTY of the item ${item.item_name} cannot be greater than ${return_item.qty}" : "A QTD do item ${item.item_name} não pode ser maior que ${return_item.qty}",
		"Selected Serial No QTY is ${item.serial_no_selected_count} it should be ${item.stock_qty}" : "A QTA selecionada do Num. de Serie é ${item.serial_no_selected_count} deveria ser ${item.stock_qty}",
		"Loyalty Point Offer Applied" : "Oferta de Pontos de Lealdade Aplicada",
		"Paid Amount" : "Valor Pago",
		"To Be Paid" : "A ser Pago",
		"Cash" : "Numerário",
		"Tax and Charges" : "Taxas e Impostos",
		"Discount Amount" : "Valor de Desconto",
		"Total Amount" : "Valor Total",
		"Totoal Amount" : "Valor Total",
		"Grand Total" : "Total Geral",
		"Back" : "Voltar",
		"Submit Payments" : "Submeter Pagamentos",
		"Give Item" : "Entregar Item",
		"New Offer Available" : "Nova Oferta Disponivel",
		"POS Offers" : "Ofertas POS",
		"Customer contact created successfully." : "Contacto de Cliente criado com sucesso.",
		"Customer Address created successfully." : "Endereço de Cliente criado com sucesso.",
		"Offer" : "Oferta",
		"Apply On" : "Aplicar Em",
		"Offer Applied" : "Oferta Aplicada",
		"Opening Amount" : "Valor de Abertura",
		"Closing Amount" : "Valor de Fecho",
		"Expected Amount" : "Valor Esperado",
		"Difference" : "Diferença",
		"Close" : "Fechar",
		"Submit" : "Submeter",
		"Closing POS Shift" : "Fechando Turno do POS",
		"Select Hold Invoice" : "Selecionar Factura em Pausa",
		"Customer Info" : "Info do Cliente",
		"Add New Address" : "Adicionar Novo Endereço",
		"New Customer" : "Novo Cliente",
		"Create POS Opening Shift" : "Criar Turno de Abertura POS",
		"Select Return Invoice" : "Selecione a Factura para Devolução",
		


	});	//HELKYD 08-07-2021