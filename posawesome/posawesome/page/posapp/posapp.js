{% include "posawesome/posawesome/page/posapp/onscan.js" %}
frappe.pages['posapp'].on_page_load = function (wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'POS Awesome',
		single_column: true
	});

	this.page.$PosApp = new frappe.PosApp.posapp(this.page);

	$('div.navbar-fixed-top').find('.container').css('padding', '0');

	$("head").append("<link href='/assets/posawesome/node_modules/vuetify/dist/vuetify.min.css' rel='stylesheet'>");
	$("head").append("<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/@mdi/font@5.x/css/materialdesignicons.min.css' />");
	$("head").append("<link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900' />");
};

//Only if PT as we are not being able to load from pt.csv
if (frappe.boot.lang == "pt") {
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
		"Card": "Cartão",
		"Offers": "Ofertas",
		"Applied": "Aplicadas",
		"There is no Customer !": "Não tem Cliente !",
		"There is no Items !": "Não tem Itens !",
		"The existing quantity of item {0} is not enough": "A quantidade existente do item {0} não é suficiente",
		"Maximum discount for Item {0} is {1}%": "Desconto Maximo para o Item {0} é {1}%",
		"Selected serial numbers of item {0} is incorrect": "Numeros de serie selecionado do item {0} é incorrecto",
		"The existing batch quantity of item {0} is not enough": "A quantidade existente do lote para o item {0} não é suficiente",
		"The discount should not be higher than {0}%": "O desconto não deve ser maior que {0}%",
		"Return Invoice Total Not Correct": "Total da Devolução da Factura não está Correcto",
		"Return Invoice Total should not be higher than {0}": "Total da Devolução da Factura não deve maior que {0}",
		"The item {0} cannot be returned because it is not in the invoice {1}": "O item {0} não pode ser devolvido porque não está na factura {1}",
		"The QTY of the item {0} cannot be greater than {1}": "A QTD do item {0} não pode ser maior que {1}",
		"Selected Serial No QTY is {0} it should be {1}": "A QTD selecionada do Num. de Serie é {0} deveria ser {1}",
		"Loyalty Point Offer Applied": "Oferta de Pontos de Lealdade Aplicada",
		"Loyalty Points": "Pontos de Lealdade",
		"Paid Amount": "Valor Pago",
		"To Be Paid": "A ser Pago",
		"Cash": "Numerário",
		"Tax and Charges": "Taxas e Impostos",
		"Discount Amount": "Valor de Desconto",
		"Total Amount": "Valor Total",
		"Totoal Amount": "Valor Total",
		"Grand Amount": "Total Geral",
		"Back": "Voltar",
		"Submit Payments": "Submeter Pagamentos",
		"Give Item": "Entregar Item",
		"New Offer Available": "Nova Oferta Disponivel",
		"POS Offers": "Ofertas POS",
		"Customer contact created successfully.": "Contacto de Cliente criado com sucesso.",
		"Customer Address created successfully.": "Endereço de Cliente criado com sucesso.",
		"Customer contact updated successfully.": "Contacto de Cliente actualizacdo com sucesso.",
		"Offer": "Oferta",
		"Apply On": "Aplicar Em",
		"Offer Applied": "Oferta Aplicada",
		"Opening Amount": "Valor de Abertura",
		"Closing Amount": "Valor de Fecho",
		"Expected Amount": "Valor Esperado",
		"Difference": "Diferença",
		"Close": "Fechar",
		"Submit": "Submeter",
		"Closing POS Shift": "Fechando Turno do POS",
		"Select Hold Invoice": "Selecionar Factura em Pausa",
		"Customer Info": "Info do Cliente",
		"Add New Address": "Adicionar Novo Endereço",
		"New Customer": "Novo Cliente",
		"Create POS Opening Shift": "Criar Turno de Abertura POS",
		"Select Return Invoice": "Selecione a Factura para Devolução",
		"Close Shift": "Fechar Turno",
		"Pages": "Paginas",
		"Customer not found": "Cliente não encontrado",
		"Customer Name": "Nome do Cliente",
		"Batch No Available QTY": "QTD Disponivel para o Lote",
		"Batch No Expiry Date": "Data de Expiração do Lote",
		"Batch No": "Num. do Lote",
		"Use Customer Credit": "Usar Crédito Cliente",
		"Is Credit Sale": "É Venda a Crédito",
		"Due Date": "Data de Expiração",
	});
}