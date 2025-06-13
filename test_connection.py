from services.firestore_service import db

usuarios_ref = db.collection("user")
docs = usuarios_ref.stream()

for doc in docs:
    print(f"{doc.id} => {doc.to_dict()}")
