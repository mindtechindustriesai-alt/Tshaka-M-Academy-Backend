"""
Firestore Service for Tshaka M Academy
Handles Firebase Admin SDK initialization and Firestore operations
"""

import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime
from firebase_admin import credentials, initialize_app, firestore, auth

# ============================================================
# GLOBAL STATE
# ============================================================
_firebase_initialized = False
db = None

# ============================================================
# INITIALIZATION
# ============================================================
def initialize_firebase() -> bool:
    """
    Initialize Firebase Admin SDK with service account credentials.
    Returns True if successful, False otherwise.
    """
    global _firebase_initialized, db
    
    # Check if already initialized
    if _firebase_initialized:
        return True
    
    # Get credentials from environment
    cred_json = os.getenv("FIREBASE_CREDENTIALS")
    if not cred_json:
        print("⚠️ FIREBASE_CREDENTIALS not found in environment variables")
        return False
    
    try:
        # Parse credentials
        cred_dict = json.loads(cred_json)
        cred = credentials.Certificate(cred_dict)
        
        # Initialize Firebase app
        initialize_app(cred)
        _firebase_initialized = True
        
        # Initialize Firestore client
        db = firestore.client()
        print("✅ Firebase Admin initialized successfully")
        print("✅ Firestore client connected")
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Invalid FIREBASE_CREDENTIALS JSON: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Firebase initialization failed: {str(e)}")
        return False

# Auto-initialize on import
initialize_firebase()

# ============================================================
# FIRESTORE OPERATIONS
# ============================================================

def get_db():
    """Get Firestore database instance. Returns None if not initialized."""
    return db

def add_document(collection_name: str, data: Dict[str, Any]) -> Optional[str]:
    """
    Add a document to a Firestore collection.
    Returns the document ID if successful, None otherwise.
    """
    if not db:
        print("⚠️ Firestore not initialized")
        return None
    try:
        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = datetime.now().isoformat()
        
        doc_ref = db.collection(collection_name).add(data)
        return doc_ref[1].id
    except Exception as e:
        print(f"❌ Error adding document to {collection_name}: {str(e)}")
        return None

def get_document(collection_name: str, doc_id: str) -> Optional[Dict[str, Any]]:
    """Get a single document by ID."""
    if not db:
        print("⚠️ Firestore not initialized")
        return None
    try:
        doc = db.collection(collection_name).document(doc_id).get()
        if doc.exists:
            return {'id': doc.id, **doc.to_dict()}
        return None
    except Exception as e:
        print(f"❌ Error fetching document {doc_id} from {collection_name}: {str(e)}")
        return None

def get_documents(
    collection_name: str,
    filters: Optional[Dict[str, Any]] = None,
    order_by: Optional[str] = None,
    direction: str = 'DESCENDING',
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Get documents from a collection with optional filters and ordering.
    """
    if not db:
        print("⚠️ Firestore not initialized")
        return []
    try:
        query = db.collection(collection_name)
        
        # Apply filters
        if filters:
            for key, value in filters.items():
                query = query.where(key, '==', value)
        
        # Apply ordering
        if order_by:
            direction_const = firestore.Query.DESCENDING if direction.upper() == 'DESCENDING' else firestore.Query.ASCENDING
            query = query.order_by(order_by, direction=direction_const)
        
        # Apply limit
        query = query.limit(limit)
        
        # Execute
        docs = query.get()
        return [{'id': doc.id, **doc.to_dict()} for doc in docs]
        
    except Exception as e:
        print(f"❌ Error fetching documents from {collection_name}: {str(e)}")
        return []

def update_document(collection_name: str, doc_id: str, data: Dict[str, Any]) -> bool:
    """Update a document."""
    if not db:
        print("⚠️ Firestore not initialized")
        return False
    try:
        # Add update timestamp
        data['updated_at'] = datetime.now().isoformat()
        db.collection(collection_name).document(doc_id).update(data)
        return True
    except Exception as e:
        print(f"❌ Error updating document {doc_id} in {collection_name}: {str(e)}")
        return False

def delete_document(collection_name: str, doc_id: str) -> bool:
    """Delete a document."""
    if not db:
        print("⚠️ Firestore not initialized")
        return False
    try:
        db.collection(collection_name).document(doc_id).delete()
        return True
    except Exception as e:
        print(f"❌ Error deleting document {doc_id} from {collection_name}: {str(e)}")
        return False

# ============================================================
# AUTHENTICATION HELPERS
# ============================================================

def verify_token(id_token: str) -> Optional[Dict[str, Any]]:
    """Verify Firebase ID token and return user data."""
    if not _firebase_initialized:
        print("⚠️ Firebase not initialized")
        return None
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        print(f"❌ Token verification failed: {str(e)}")
        return None

def get_user_role(uid: str) -> Optional[str]:
    """Get user role from Firestore."""
    if not db:
        return None
    try:
        doc = db.collection('users').document(uid).get()
        if doc.exists:
            return doc.to_dict().get('role', 'student')
        return None
    except Exception as e:
        print(f"❌ Error fetching user role: {str(e)}")
        return None

def set_user_role(uid: str, role: str, data: Optional[Dict] = None) -> bool:
    """Set user role and additional data in Firestore."""
    if not db:
        return False
    try:
        user_data = {
            'role': role,
            'updated_at': datetime.now().isoformat(),
            **(data or {})
        }
        db.collection('users').document(uid).set(user_data, merge=True)
        return True
    except Exception as e:
        print(f"❌ Error setting user role: {str(e)}")
        return False

def get_user_data(uid: str) -> Optional[Dict[str, Any]]:
    """Get full user data from Firestore."""
    if not db:
        return None
    try:
        doc = db.collection('users').document(uid).get()
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception as e:
        print(f"❌ Error fetching user data: {str(e)}")
        return None

# ============================================================
# CHAT HISTORY HELPERS
# ============================================================

def save_chat_message(
    user_id: str,
    message: str,
    response: str,
    grade: str = "General",
    subject: str = "General",
    role: str = "student",
    source: str = "deepseek"
) -> Optional[str]:
    """Save a chat interaction to Firestore."""
    data = {
        'user_id': user_id,
        'message': message,
        'response': response,
        'grade': grade,
        'subject': subject,
        'role': role,
        'source': source,
        'timestamp': datetime.now().isoformat()
    }
    return add_document('chat_history', data)

def get_chat_history(
    user_id: str,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """Get chat history for a user."""
    return get_documents(
        'chat_history',
        filters={'user_id': user_id},
        order_by='timestamp',
        direction='DESCENDING',
        limit=limit
    )

# ============================================================
# QUIZ HELPERS
# ============================================================

def save_quiz_result(
    student_id: str,
    subject: str,
    score: int,
    total_questions: int,
    level: str = "medium"
) -> Optional[str]:
    """Save a quiz result to Firestore."""
    data = {
        'student_id': student_id,
        'subject': subject,
        'score': score,
        'total_questions': total_questions,
        'percentage': round((score / total_questions) * 100, 2) if total_questions > 0 else 0,
        'level': level,
        'timestamp': datetime.now().isoformat()
    }
    return add_document('quiz_results', data)

def get_student_performance(
    student_id: str,
    subject: Optional[str] = None,
    limit: int = 10
) -> List[Dict[str, Any]]:
    """Get student performance data."""
    filters = {'student_id': student_id}
    if subject:
        filters['subject'] = subject
    return get_documents(
        'quiz_results',
        filters=filters,
        order_by='timestamp',
        direction='DESCENDING',
        limit=limit
    )

# ============================================================
# UPLOAD HELPERS
# ============================================================

def save_upload(
    student_id: str,
    file_name: str,
    file_type: str,
    file_size: int,
    file_url: str,
    subject: str,
    grade: str,
    topic: Optional[str] = None,
    analysis: Optional[Dict] = None
) -> Optional[str]:
    """Save file upload metadata to Firestore."""
    data = {
        'student_id': student_id,
        'file_name': file_name,
        'file_type': file_type,
        'file_size': file_size,
        'file_url': file_url,
        'subject': subject,
        'grade': grade,
        'topic': topic or 'General',
        'analysis': analysis or {},
        'timestamp': datetime.now().isoformat()
    }
    return add_document('uploads', data)

def get_uploads(
    student_id: str,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """Get upload history for a student."""
    return get_documents(
        'uploads',
        filters={'student_id': student_id},
        order_by='timestamp',
        direction='DESCENDING',
        limit=limit
    )

# ============================================================
# WHATSAPP HELPERS
# ============================================================

def log_whatsapp_message(
    group_id: str,
    message: str,
    sender_id: str,
    sender_role: str,
    status: str = "sent"
) -> Optional[str]:
    """Log WhatsApp message to Firestore."""
    data = {
        'group_id': group_id,
        'message': message,
        'sender_id': sender_id,
        'sender_role': sender_role,
        'status': status,
        'timestamp': datetime.now().isoformat()
    }
    return add_document('whatsapp_logs', data)

# ============================================================
# INC0GNITO HELPERS
# ============================================================

def create_incognito_session(student_id: str, reason: str = "privacy") -> Optional[str]:
    """Create an incognito session for a student."""
    anonymous_id = f"anon_{student_id[:8]}_{int(datetime.now().timestamp())}"
    data = {
        'student_id': student_id,
        'anonymous_id': anonymous_id,
        'reason': reason,
        'active': True,
        'timestamp': datetime.now().isoformat()
    }
    doc_id = add_document('incognito_sessions', data)
    return anonymous_id if doc_id else None

# ============================================================
# EXPORTS
# ============================================================
# Make sure db is available for import
__all__ = [
    'db',
    'get_db',
    'initialize_firebase',
    'verify_token',
    'get_user_role',
    'set_user_role',
    'get_user_data',
    'add_document',
    'get_document',
    'get_documents',
    'update_document',
    'delete_document',
    'save_chat_message',
    'get_chat_history',
    'save_quiz_result',
    'get_student_performance',
    'save_upload',
    'get_uploads',
    'log_whatsapp_message',
    'create_incognito_session'
]
