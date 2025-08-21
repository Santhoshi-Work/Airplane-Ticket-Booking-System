// frappe.pages['shop-details'].on_page_load = function(wrapper) {
// 	var page = frappe.ui.make_app_page({
// 		parent: wrapper,
// 		title: 'Details of Individual Shop',
// 		single_column: true
// 	});
frappe.pages['shop-details'].on_page_load = function(wrapper) {
    let page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Shop Details',
        single_column: true
    });
	page.set_title_sub('Subtitle')
	page.set_indicator('testing', 'purple')
	let addBtn = page.set_primary_action(
    '+ Add New Shop Detail',
    () => create_new(),
    'octicon octicon-plus'
);

refreshBtn = page.set_secondary_action('Refresh', () => refresh(), 'refresh');

page.add_menu_item('Menu Option', () => open_email_dialog());

let field = page.add_field({
 label: 'Status',
 fieldtype: 'Select',
 fieldname: 'status',
 options: [
 'Open',
 'Closed',
 'Cancelled'
 ],
 change() {
 console.log(field.get_value());
 }
});





}

	// page.set_title('My Page')
	// page.set_title_sub('Subtitle')

    // // Add simple content
    // $(wrapper).find('.layout-main').append(`
    //     <h2>Welcome to Shop Details Page</h2>
    //     <p>This is a very simple sample page created using Frappe Page API.</p>
    // `);
// }