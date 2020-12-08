from neo4j import GraphDatabase, basic_auth
import socket


class Movie_queries(object):
    def __init__(self, password):
        self.driver = GraphDatabase.driver("bolt://localhost", auth=("neo4j", password), encrypted=False)
        self.session = self.driver.session()
        self.transaction = self.session.begin_transaction()

    def q0(self):
        result = self.transaction.run("""
            MATCH (n:Actor) RETURN n.name, n.id ORDER BY n.birthday ASC LIMIT 3
        """)
        return [(r[0], r[1]) for r in result]

    def q1(self):
        result = self.transaction.run("""
    MATCH (n:Actor)-[:ACTS_IN]->(m:Movie) RETURN n.name, count(m.title)
order by count(m.title) desc, n.name asc limit 20
        """)
        return [(r[0], r[1]) for r in result]

    def q2(self):
        result = self.transaction.run("""
        MATCH (n:Actor)-[:ACTS_IN]->(m:Movie) <-[:RATED]-() with m, 
        count(distinct n.name) AS actor_count order 
        by  actor_count desc return m.title, actor_count limit 1  
        """)
        return [(r[0], r[1]) for r in result]

    def q3(self):
        result = self.transaction.run("""
       MATCH(m:Movie) <-[:DIRECTED]- (d:Director)  
with  d, count(distinct m.genre) as num_genre
where num_genre > 1
return d.name, num_genre
order by num_genre desc, d.name asc 
        """)
        return [(r[0], r[1]) for r in result]

    def q4(self):
        result = self.transaction.run("""
    MATCH (a:Actor{name: "Kevin Bacon"})-[:ACTS_IN]->(m:Movie)<-[:ACTS_IN]-(b:Actor)
MATCH (b:Actor)-[:ACTS_IN]->(n:Movie)<-[:ACTS_IN]-(c:Actor)
WHERE c <> a AND NOT (a)-[:ACTS_IN]->()<-[:ACTS_IN]-(c)
RETURN distinct c.name 
order by c.name
       """)
        return [(r[0]) for r in result]

if __name__ == "__main__":
    sol = Movie_queries("neo4jpass")
    print("---------- Q0 ----------")
    print(sol.q0())
    print("---------- Q1 ----------")
    print(sol.q1())
    print("---------- Q2 ----------")
    print(sol.q2())
    print("---------- Q3 ----------")
    print(sol.q3())
    print("---------- Q4 ----------")
    print(sol.q4())
    sol.transaction.close()
    sol.session.close()
    sol.driver.close()

