from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Time, Date
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    active = Column(Boolean, nullable=False, default=True)

class Bus(Base):
    __tablename__ = "buses"

    gos_number = Column(String(10), primary_key=True)
    capacity = Column(Integer, nullable=False)
    is_air_conditioner = Column(Boolean, nullable=False)

    # def __repr__(self):
    #     return f"<Bus(gos_number={self.gos_number}, capasity={self.capacity}, is_air_cond={self.is_air_conditioner})>"

class Company(Base):
    __tablename__ = "company"

    name = Column(String(50), primary_key=True)
    duration_work = Column(Integer, nullable=False)
    address = Column(String(100), nullable=False)
    number_phone = Column(String(11))


class BusesInCompany(Base):
    __tablename__ = "buses_in_company"

    buses_gos_number = Column(String(10), ForeignKey('buses.gos_number'), primary_key=True)
    company_name = Column(String(50), ForeignKey('company.name'), primary_key=True)


class Driver(Base):
    __tablename__ = "drivers"

    number_vy = Column(Integer, primary_key=True)
    fio = Column(String(100), nullable=False)
    experience = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)


class DelaysVoyage(Base):
    __tablename__ = "delays_voyage"

    id = Column(Integer, primary_key=True)
    number_vy = Column(Integer, ForeignKey('drivers.number_vy'))
    cause = Column(String(100), nullable=False)
    duration = Column(Time, nullable=False)


class ReportIncomeCompany(Base):
    __tablename__ = "report_income_company"

    id = Column(Integer, primary_key=True)
    company_name = Column(String(50), ForeignKey('company.name'))
    start_period = Column(Date, nullable=False)
    end_period = Column(Date, nullable=False)
    revenue = Column(Integer, nullable=False)
    expenses = Column(Integer, nullable=False)
    profit = Column(Integer, nullable=False)


class TypeRepair(Base):
    __tablename__ = "type_repair"

    id = Column(Integer, primary_key=True)
    detail = Column(String(50), unique=True, nullable=False)
    cost_detail = Column(Integer, nullable=False)


class OrderRepair(Base):
    __tablename__ = "order_repair"

    id = Column(Integer, primary_key=True)
    buses_gos_number = Column(String(10), ForeignKey('buses.gos_number'))
    detail_name = Column(String(50), ForeignKey('type_repair.detail'))
    date = Column(Date, nullable=False)


class Stop(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)


class Route(Base):
    __tablename__ = "routes"

    number_route = Column(String(10), primary_key=True)
    count_stops = Column(Integer, nullable=False)
    start_stop = Column(String(50), ForeignKey('stops.name'))
    end_stop = Column(String(50), ForeignKey('stops.name'))
    time_start = Column(Time, nullable=False)
    time_end = Column(Time, nullable=False)
    cost_travel = Column(Integer, nullable=False)


class StopsAndRoutes(Base):
    __tablename__ = "stops_and_routes"

    id_stops = Column(Integer, ForeignKey('stops.id'), primary_key=True)
    number_route = Column(String(10), ForeignKey('routes.number_route'), primary_key=True)


class Passenger(Base):
    __tablename__ = "passengers"

    id = Column(Integer, primary_key=True)
    fio = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    id_passenger = Column(Integer, ForeignKey('passengers.id'))
    cost_travel = Column(Integer, nullable=False)
    date_start = Column(Date, nullable=False)
    start_stop = Column(String(50), ForeignKey('stops.name'))
    end_stop = Column(String(50), ForeignKey('stops.name'))


class RouteSheet(Base):
    __tablename__ = "route_sheet"

    id = Column(Integer, primary_key=True)
    number_vy = Column(Integer, ForeignKey('drivers.number_vy'))
    number_route = Column(String(10), ForeignKey('routes.number_route'))
    date = Column(Date, nullable=False)
    gos_number_bus = Column(String(10), ForeignKey('buses.gos_number'))


class ReviewPassenger(Base):
    __tablename__ = "review_passenger"

    id = Column(Integer, primary_key=True)
    id_passenger = Column(Integer, ForeignKey('passengers.id'))
    gos_number_bus = Column(String(10), ForeignKey('buses.gos_number'))
    grade = Column(Integer, nullable=False)
    text_review = Column(String(500))
    date = Column(Date, nullable=False)




# from sqlalchemy import Column, Integer, String, Boolean
# from app.database import Base
#
# class Bus(Base):
#     __tablename__ = "busestest"
#
#     gos_number = Column(String(10), primary_key=True)
#     capacity = Column(Integer, nullable=False)
#     is_air_conditioner = Column(Boolean, nullable=False)
#
#     def __repr__(self):
#         return f"<Bus(gos_number={self.gos_number}, capasity={self.capacity}, is_air_cond={self.is_air_conditioner})>"