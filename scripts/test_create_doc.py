from core.models import Document
from django.contrib.auth.models import User

u = User.objects.first()
Document.objects.create(
    title='Sample Test Doc',
    file='documents/test-doc.txt',
    description='Created by test script',
    uploaded_by=u if u else None
)
print('DOC_CREATED')
