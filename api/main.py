from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from . import database, schemas
import os

app = FastAPI(
    title="Medical Telegram Warehouse API",
    description="Analytical API for Ethiopian medical business insights from Telegram data.",
    version="1.0.0"
)

@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def get_top_products(limit: int = 10, db: Session = Depends(database.get_db)):
    """
    Returns the most frequently mentioned terms/products across all channels.
    Note: This is a simplified example assuming we extract products or use simple word frequency.
    For a real use case, we'd query the 'fct_messages' or a dedicated derived table.
    """
    try:
        # Simplified query: grouping by message text (in reality, you'd want extracted entities)
        # This is strictly a placeholder query structure.
        # Ideally, you have a table or view 'mart_top_products'
        query = text("""
            SELECT 
                substring(message_text from 1 for 20) as product_name, 
                count(*) as mention_count
            FROM fct_messages
            GROUP BY 1
            ORDER BY 2 DESC
            LIMIT :limit
        """)
        result = db.execute(query, {"limit": limit}).fetchall()
        return [{"product_name": row[0], "mention_count": row[1]} for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/channels/{channel_name}/activity", response_model=schemas.ChannelActivity)
def get_channel_activity(channel_name: str, db: Session = Depends(database.get_db)):
    """
    Returns posting activity and trends for a specific channel.
    """
    try:
        query = text("""
            SELECT 
                c.channel_name,
                COUNT(m.message_id) as total_messages,
                AVG(m.view_count) as avg_views
            FROM fct_messages m
            JOIN dim_channels c ON m.channel_key = c.channel_key
            WHERE c.channel_name = :channel_name
            GROUP BY c.channel_name
        """)
        result = db.execute(query, {"channel_name": channel_name}).first()
        if not result:
            raise HTTPException(status_code=404, detail="Channel not found")
        return {"channel_name": result[0], "total_messages": result[1], "avg_views": result[2]}
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/messages", response_model=List[schemas.MessageResponse])
def search_messages(query: str, limit: int = 20, db: Session = Depends(database.get_db)):
    """
    Searches for messages containing a specific keyword.
    """
    try:
        sql = text("""
            SELECT 
                m.message_id, 
                c.channel_name, 
                d.full_date as date, 
                m.message_text as text, 
                m.view_count as views
            FROM fct_messages m
            JOIN dim_channels c ON m.channel_key = c.channel_key
            JOIN dim_dates d ON m.date_key = d.date_key
            WHERE m.message_text ILIKE :search_query
            LIMIT :limit
        """)
        result = db.execute(sql, {"search_query": f"%{query}%", "limit": limit}).fetchall()
        
        return [
            {
                "message_id": row[0],
                "channel_name": row[1],
                "date": row[2],
                "text": row[3],
                "views": row[4]
            }
            for row in result
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reports/visual-content", response_model=List[schemas.VisualContentStats])
def get_visual_content_stats(db: Session = Depends(database.get_db)):
    """
    Returns statistics about image usage across channels.
    """
    try:
        query = text("""
            SELECT 
                c.channel_name,
                COUNT(m.message_id) FILTER (WHERE m.has_image = true) as image_count
            FROM fct_messages m
            JOIN dim_channels c ON m.channel_key = c.channel_key
            GROUP BY c.channel_name
        """)
        result = db.execute(query).fetchall()
        return [{"channel_name": row[0], "image_count": row[1]} for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
