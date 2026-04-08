# Database Schema

## users_user
- `id`
- `email`
- `username`
- `password`
- `first_name`
- `last_name`
- `phone`
- `avatar`
- `role`
- `created_at`
- `updated_at`

## catalog_category
- `id`
- `name`
- `slug`
- `created_at`
- `updated_at`

## catalog_product
- `id`
- `seller_id`
- `category_id`
- `title`
- `slug`
- `description`
- `price`
- `stock`
- `is_active`
- `created_at`
- `updated_at`

## catalog_productimage
- `id`
- `product_id`
- `image`
- `is_primary`

## catalog_discount
- `id`
- `product_id`
- `percentage`
- `starts_at`
- `ends_at`

## cart_cart
- `id`
- `user_id`

## cart_cartitem
- `id`
- `cart_id`
- `product_id`
- `quantity`

## orders_order
- `id`
- `user_id`
- `status`
- `total_amount`
- `shipping_address`

## orders_orderitem
- `id`
- `order_id`
- `product_id`
- `quantity`
- `unit_price`

## payments_paymenttransaction
- `id`
- `order_id`
- `provider`
- `status`
- `amount`
- `external_reference`

## reviews_review
- `id`
- `product_id`
- `user_id`
- `rating`
- `comment`

## notifications_notification
- `id`
- `user_id`
- `title`
- `message`
- `notification_type`
- `is_read`
