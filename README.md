
Endpoints:

- auth: http://localhost/shopify/auth/\<store-link-including-.com\>
- auth should redirect to -> http://localhost/shopify/done (configure your app as such)
- api-call : http://localhost/shopify/\<store-link-including-.com\>/get-products

-view-all-stores: http://localhost/shopify/stores




Examples:

- auth: http://localhost/shopify/auth/simple-store-dev-0mn7bd5v.myshopify.com
- api-call : http://localhost/shopify/simple-store-dev-0mn7bd5v.myshopify.com/get-products

-view-all-stores: http://localhost/shopify/stores