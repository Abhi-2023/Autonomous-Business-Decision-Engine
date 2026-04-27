from backend.db.base import Base
import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    String, DateTime, Text, Float, Integer,
    ForeignKey, PrimaryKeyConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Customer(Base):
    __tablename__ = "customers"

    customer_id:     Mapped[str] = mapped_column(String(50), primary_key=True)
    unique_id:       Mapped[str] = mapped_column(String(50))
    zip_code_prefix: Mapped[Optional[str]] = mapped_column(String(10))
    city:            Mapped[Optional[str]] = mapped_column(String(100))
    state:           Mapped[Optional[str]] = mapped_column(String(2))

    orders: Mapped[List["Order"]] = relationship("Order", back_populates="customer")

    def __repr__(self):
        return f"<Customer {self.customer_id}>"


class Geolocation(Base):
    __tablename__ = "geolocations"

    geolocation_id:  Mapped[str]   = mapped_column(String(36), primary_key=True,
                                        default=lambda: str(uuid.uuid4()))
    zip_code_prefix: Mapped[str]   = mapped_column(String(10))
    latitude:        Mapped[float] = mapped_column(Float)
    longitude:       Mapped[float] = mapped_column(Float)
    city:            Mapped[Optional[str]] = mapped_column(String(100))
    state:           Mapped[Optional[str]] = mapped_column(String(2))

    def __repr__(self):
        return f"<Geolocation zip={self.zip_code_prefix}>"


class Seller(Base):
    __tablename__ = "sellers"

    seller_id: Mapped[str]          = mapped_column(String(50), primary_key=True)
    city:      Mapped[Optional[str]] = mapped_column(String(100))
    state:     Mapped[Optional[str]] = mapped_column(String(2))

    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="seller")

    def __repr__(self):
        return f"<Seller {self.seller_id}>"


class Product(Base):
    __tablename__ = "products"

    product_id:         Mapped[str]          = mapped_column(String(50), primary_key=True)
    category_name:      Mapped[Optional[str]] = mapped_column(String(100))
    category_name_en:   Mapped[Optional[str]] = mapped_column(String(100))
    description_length: Mapped[Optional[int]] = mapped_column(Integer)
    description:        Mapped[Optional[str]] = mapped_column(Text)  # used by RAG

    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product {self.product_id}>"


class Order(Base):
    __tablename__ = "orders"

    order_id:                     Mapped[str]            = mapped_column(String(50), primary_key=True)
    customer_id:                  Mapped[str]            = mapped_column(ForeignKey("customers.customer_id"))
    order_status:                 Mapped[str]            = mapped_column(String(50))
    order_purchase_timestamp:     Mapped[datetime]       = mapped_column(DateTime(timezone=True))
    order_approved_at:            Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    order_delivered_carrier_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    order_delivered_customer_date:Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    order_estimated_delivery_date:Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    customer: Mapped["Customer"]        = relationship("Customer", back_populates="orders")
    items:    Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order")
    payments: Mapped[List["OrderPayment"]] = relationship("OrderPayment", back_populates="order")
    reviews:  Mapped[List["OrderReview"]]  = relationship("OrderReview", back_populates="order")

    def __repr__(self):
        return f"<Order {self.order_id}>"


class OrderItem(Base):
    __tablename__ = "order_items"
    __table_args__ = (
        PrimaryKeyConstraint("order_id", "order_item_id"),
    )

    order_id:            Mapped[str]      = mapped_column(ForeignKey("orders.order_id"))
    order_item_id:       Mapped[int]      = mapped_column(Integer)
    product_id:          Mapped[str]      = mapped_column(ForeignKey("products.product_id"))
    seller_id:           Mapped[str]      = mapped_column(ForeignKey("sellers.seller_id"))
    shipping_limit_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    price:               Mapped[float]   = mapped_column(Float)
    freight_value:       Mapped[float]   = mapped_column(Float)

    order:   Mapped["Order"]   = relationship("Order",   back_populates="items")
    product: Mapped["Product"] = relationship("Product", back_populates="items")
    seller:  Mapped["Seller"]  = relationship("Seller",  back_populates="items")

    def __repr__(self):
        return f"<OrderItem order={self.order_id} item={self.order_item_id}>"


class OrderPayment(Base):
    __tablename__ = "order_payments"
    __table_args__ = (
        PrimaryKeyConstraint("order_id", "payment_sequential"),
    )

    order_id:             Mapped[str]   = mapped_column(ForeignKey("orders.order_id"))
    payment_sequential:   Mapped[int]   = mapped_column(Integer)
    payment_type:         Mapped[str]   = mapped_column(String(50))
    payment_installments: Mapped[int]   = mapped_column(Integer)
    payment_value:        Mapped[float] = mapped_column(Float)

    order: Mapped["Order"] = relationship("Order", back_populates="payments")

    def __repr__(self):
        return f"<Payment order={self.order_id} seq={self.payment_sequential}>"


class OrderReview(Base):
    __tablename__ = "order_reviews"

    order_review_id: Mapped[str]          = mapped_column(String(50), primary_key=True)
    order_id:        Mapped[str]          = mapped_column(ForeignKey("orders.order_id"))
    review_score:    Mapped[int]          = mapped_column(Integer)
    review_comment:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    order: Mapped["Order"] = relationship("Order", back_populates="reviews")

    def __repr__(self):
        return f"<Review {self.order_review_id}>"