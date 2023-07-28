import pandas as pd
from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint
from app import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastName = db.Column(db.String(150))
    notes = db.relationship('Note')


# Define the Service model


class Service(db.Model):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    location_type = Column(String)
    facility_title = Column(String)
    address = Column(String)
    phone = Column(String)
    hours_open_to_public = Column(String)
    hours_closed = Column(String)
    service_description = Column(String)

# Function to store the data in the database


def store_data(location_type, facility_title, address, phone, hours_open_to_public, hours_closed, service_description):
    existing_record = Service.query.filter(
        (Service.address == address) |
        (Service.phone == phone) |
        (Service.facility_title == facility_title)
    ).first()

    if existing_record:
        return False

    new_business = Service(
        location_type=location_type,
        facility_title=facility_title,
        address=address,
        phone=phone,
        hours_open_to_public=hours_open_to_public,
        hours_closed=hours_closed,
        service_description=service_description
    )
    db.session.add(new_business)
    db.session.commit()
    return True

# model to store web scrape in to a database


class WebResults(db.Model):
    __tablename__ = "webresults"
    id = Column(Integer, primary_key=True)
    query = Column(String)
    rank = Column(Integer)
    link = Column(String)
    title = Column(String)
    snippet = Column(String)
    html = Column(String)
    created = Column(DateTime)
    relevance = Column(Integer)

    __table_args__ = (UniqueConstraint(
        'query', 'link', name='_query_link_uc'),)

    def query_results(self, query):
        df = pd.read_sql(
            f"select * from webresults where query ='{query}' order by rank asc;", db.engine)
        return df

    def insert_row(self, values):
        try:
            result = WebResults(**values)
            db.session.add(result)
            db.session.commit()
        except:
            db.session.rollback()

    def update_relevance(self, query, link, relevance):
        try:
            db.session.query(WebResults).filter_by(
                query=query, link=link).update({"relevance": relevance})
            db.session.commit()
        except:
            db.session.rollback()
