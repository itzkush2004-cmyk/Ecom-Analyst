import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = None

def _get_client():
    global client
    if client is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable not set. "
                "Please add it to your .env file or Streamlit secrets."
            )
        client = Groq(api_key=api_key)
    return client

SCHEMA = """
Database: Supabase PostgreSQL

Tables and columns:

olist_orders_dataset (order_id varchar, customer_id varchar, order_status varchar, order_purchase_timestamp varchar, order_approved_at varchar, order_delivered_carrier_date varchar, order_delivered_customer_date varchar, order_estimated_delivery_date varchar)

olist_order_items_dataset (order_id varchar, order_item_id integer, product_id varchar, seller_id varchar, shipping_limit_date varchar, price float, freight_value float)

olist_products_dataset (product_id varchar, product_category_name varchar, product_name_lenght integer, product_description_lenght integer, product_photos_qty integer, product_weight_g varchar, product_length_cm varchar, product_height_cm varchar, product_width_cm varchar)

olist_order_reviews_dataset (review_id varchar, order_id varchar, review_score integer, review_comment_title varchar, review_comment_message varchar, review_creation_date varchar, review_answer_timestamp varchar)

olist_order_payments_dataset (order_id varchar, payment_sequential integer, payment_type varchar, payment_installments integer, payment_value float)

olist_sellers_dataset (seller_id varchar, seller_zip_code_prefix varchar, seller_city varchar, seller_state varchar)

olist_customers_dataset (customer_id varchar, customer_unique_id varchar, customer_zip_code_prefix varchar, customer_city varchar, customer_state varchar)

olist_geolocation_dataset (geolocation_zip_code_prefix varchar, geolocation_lat float, geolocation_lng float, geolocation_city varchar, geolocation_state varchar)

product_category_name_translation (product_category_name varchar, product_category_name_english varchar)

Key relationships:
- olist_orders_dataset.order_id = olist_order_items_dataset.order_id
- olist_order_items_dataset.product_id = olist_products_dataset.product_id
- olist_orders_dataset.order_id = olist_order_reviews_dataset.order_id
- olist_orders_dataset.order_id = olist_order_payments_dataset.order_id
- olist_order_items_dataset.seller_id = olist_sellers_dataset.seller_id
- olist_orders_dataset.customer_id = olist_customers_dataset.customer_id
- olist_products_dataset.product_category_name = product_category_name_translation.product_category_name
"""

SYSTEM_PROMPT = f"""
You are a PostgreSQL expert and data analyst. Your job is to answer business questions strictly using data from the database.

Rules:
- You must ALWAYS generate a SQL SELECT query to answer the question — even for follow-up questions.
- Use conversation history to understand context for follow-up questions.
- Only generate SELECT statements. Never use INSERT, UPDATE, DELETE, DROP, or any DDL.
- Use exact table names as provided in the schema — no prefix needed e.g. olist_orders_dataset
- Return ONLY the SQL query, no explanation, no markdown, no code fences.
- Use LIMIT instead of TOP for row limiting e.g. LIMIT 10
- Use proper JOINs when the question requires data from multiple tables.
- Always use table aliases for readability.
- Always alias every column in SELECT with a meaningful name using AS e.g. COUNT(DISTINCT o.order_id) AS total_orders
- When using AVG() on integer columns, always CAST to float first e.g. AVG(CAST(r.review_score AS float))
- product_weight_g, product_length_cm, product_height_cm, product_width_cm are stored as varchar — do not use them in numeric aggregations unless explicitly asked.
- Always JOIN product_category_name_translation on product_category_name to return English category names. Use product_category_name_english in SELECT instead of product_category_name.
- If the question cannot be answered from the database, return exactly this text: CANNOT_ANSWER

Date handling rules (CRITICAL):
- ALL date columns are stored as varchar in the database — order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date, shipping_limit_date, review_creation_date, review_answer_timestamp
- ALWAYS cast date columns before using any date function: CAST(o.order_purchase_timestamp AS timestamp)
- For year filtering: EXTRACT(YEAR FROM CAST(o.order_purchase_timestamp AS timestamp)) = 2018
- For month filtering: EXTRACT(MONTH FROM CAST(o.order_purchase_timestamp AS timestamp))
- For delivery time calculation: CAST(o.order_delivered_customer_date AS timestamp) - CAST(o.order_purchase_timestamp AS timestamp)
- For delivery time in days use: EXTRACT(EPOCH FROM (CAST(o.order_delivered_customer_date AS timestamp) - CAST(o.order_purchase_timestamp AS timestamp))) / 86400
- Never use EXTRACT or any date function directly on a varchar column without CAST first
- Always filter out NULL values when casting dates: WHERE o.order_purchase_timestamp IS NOT NULL

Database schema:
{SCHEMA}
"""

def generate_sql(question: str, conversation_history: list = []) -> str:
    groq_client = _get_client()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for turn in conversation_history:
        messages.append({"role": "user", "content": turn["question"]})
        messages.append({"role": "assistant", "content": f"SQL: {turn['sql']}\nResult: {turn['result']}"})

    messages.append({"role": "user", "content": question})

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0
    )
    sql = response.choices[0].message.content.strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql


if __name__ == "__main__":
    question = "Show me monthly order volume trends for 2018"
    sql = generate_sql(question)
    print(sql)