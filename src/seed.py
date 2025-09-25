import logging
from src.database import SessionLocal
from src.models import Product, Team, Service, Project, Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_data():
    db = SessionLocal()
    try:
        # Check if data already exists
        if db.query(Product).first():
            logger.info("Database already seeded.")
            return

        logger.info("Seeding database with initial data...")

        # Create Products
        product1 = Product(name="Data Platform")
        product2 = Product(name="Customer Engagement")
        db.add_all([product1, product2])
        db.commit()

        # Create Teams
        team1 = Team(name="Data Engineering", product_id=product1.id)
        team2 = Team(name="Analytics", product_id=product1.id)
        team3 = Team(name="Marketing Tech", product_id=product2.id)
        db.add_all([team1, team2, team3])
        db.commit()

        # Create Services
        service1 = Service(name="Data Warehouse", team_id=team1.id)
        service2 = Service(name="ETL Service", team_id=team1.id)
        service3 = Service(name="BI Tool", team_id=team2.id)
        service4 = Service(name="Email Service", team_id=team3.id)
        db.add_all([service1, service2, service3, service4])
        db.commit()

        # Create Projects
        project1 = Project(name="Q3 Reporting Dashboard")
        db.add(project1)
        db.commit()

        # Create Configs
        config1 = Config(name="Production DW Config", service_id=service1.id)
        db.add(config1)
        db.commit()

        logger.info("Database seeding complete.")

    finally:
        db.close()

if __name__ == "__main__":
    seed_data()