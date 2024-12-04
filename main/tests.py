from django.test import SimpleTestCase
from django.urls import reverse, resolve
from main.views import home, search, category_list, brand_list, product_list, category_product_list, brand_product_list, product_detail, filter_data, load_more_data, add_to_cart, cart_list, delete_cart_item, update_cart_item, signup, checkout, save_review, my_dashboard, my_orders, my_order_items, add_wishlist, my_wishlist, my_reviews, my_addressbook, save_address, activate_address, update_address, edit_profile, payment, delete_wishlist

class MainAppUrlsTest(SimpleTestCase):
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, home)

    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEqual(resolve(url).func, search)

    def test_category_list_url_resolves(self):
        url = reverse('category-list')
        self.assertEqual(resolve(url).func, category_list)
        
    def test_brand_list_url_resolves(self):
        url = reverse('brand-list')
        self.assertEqual(resolve(url).func, brand_list)
        
    def test_product_list_url_resolves(self):
        url = reverse('product-list')
        self.assertEqual(resolve(url).func, product_list)
        
    def test_category_product_list_url_resolves(self):
        url = reverse('category-product-list', args=[1])
        self.assertEqual(resolve(url).func, category_product_list)
        
    def test_brand_product_list_url_resolves(self):
        url = reverse('brand-product-list', args=[1])
        self.assertEqual(resolve(url).func, brand_product_list)
        
    def test_product_detail_url_resolves(self):
        url = reverse('product_detail', args=['Acer Aspire VX5-591G', 33])
        self.assertEqual(resolve(url).func, product_detail)
        
    def test_filter_data_url_resolves(self):
        url = reverse('filter_data')
        self.assertEqual(resolve(url).func, filter_data)
        
    def test_load_more_data_url_resolves(self):
        url = reverse('load_more_data')
        self.assertEqual(resolve(url).func, load_more_data)
        
    def test_add_to_cart_url_resolves(self):
        url = reverse('add_to_cart')
        self.assertEqual(resolve(url).func, add_to_cart)
        
    def test_cart_list_url_resolves(self):
        url = reverse('cart')
        self.assertEqual(resolve(url).func, cart_list)
        
    def test_delete_cart_item_url_resolves(self):
        url = reverse('delete-from-cart')
        self.assertEqual(resolve(url).func, delete_cart_item)
        
    def test_update_cart_item_url_resolves(self):
        url = reverse('update-cart')
        self.assertEqual(resolve(url).func, update_cart_item)
        
    def test_signup_url_resolves(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, signup)
        
    def test_checkout_url_resolves(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, checkout)
        
    def test_save_review_url_resolves(self):
        url = reverse('save-review', args=[1])
        self.assertEqual(resolve(url).func, save_review)
        
    def test_my_dashboard_url_resolves(self):
        url = reverse('my_dashboard')
        self.assertEqual(resolve(url).func, my_dashboard)
        
    def test_my_orders_url_resolves(self):
        url = reverse('my_orders')
        self.assertEqual(resolve(url).func, my_orders)
        
    def test_my_order_items_url_resolves(self):
        url = reverse('my_order_items', args=[28])
        self.assertEqual(resolve(url).func, my_order_items)
        
    def test_add_wishlist_url_resolves(self):
        url = reverse('add_wishlist')
        self.assertEqual(resolve(url).func, add_wishlist)
        
    def test_my_wishlist_url_resolves(self):
        url = reverse('my_wishlist')
        self.assertEqual(resolve(url).func, my_wishlist)
        
    def test_my_reviews_url_resolves(self):
        url = reverse('my-reviews')
        self.assertEqual(resolve(url).func, my_reviews)
        
    def test_my_addressbook_url_resolves(self):
        url = reverse('my-addressbook')
        self.assertEqual(resolve(url).func, my_addressbook)
        
    def test_save_address_url_resolves(self):
        url = reverse('add-address')
        self.assertEqual(resolve(url).func, save_address)
        
    def test_activate_address_url_resolves(self):
        url = reverse('activate-address')
        self.assertEqual(resolve(url).func, activate_address)
        
    def test_update_address_url_resolves(self):
        url = reverse('update-address', args=[4])
        self.assertEqual(resolve(url).func, update_address)
        
    def test_edit_profile_url_resolves(self):
        url = reverse('edit-profile')
        self.assertEqual(resolve(url).func, edit_profile)
        
    def test_payment_url_resolves(self):
        url = reverse('payment')
        self.assertEqual(resolve(url).func, payment)
        
    def test_delete_wishlist_url_resolves(self):
        url = reverse('delete-wishlist')
        self.assertEqual(resolve(url).func, delete_wishlist)