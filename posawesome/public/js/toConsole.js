$(function() {
	frappe.realtime.on('toconsole', function(data) {
		data.forEach(element => {
			console.log(element);
		});
	});
});