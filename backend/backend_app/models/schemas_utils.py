# backend/backend_app/models/schema_utils.py
from backend_app.models.schemas import ChromaStudentMetadata, UserProfile

def user_profile_to_chroma_metadata(profile: UserProfile) -> ChromaStudentMetadata:
    """
    Converts a UserProfile instance (Supabase) into a ChromaStudentMetadata instance.
    Note: Mapping 'location' -> 'current_location' and 'stage' -> 'company_stage'.
    """
    return ChromaStudentMetadata(
        user_id=profile.user_id,
        full_name=profile.full_name,
        university=profile.university,
        major=profile.major,
        current_location=profile.location,       # mapping from UserProfile.location
        country=None,                            # not available in UserProfile; set as None or default as needed
        company_stage=profile.stage,             # mapping from UserProfile.stage
        skills=profile.skills or [],
        interests=profile.interests or [],
        most_impressive_fact=profile.most_impressive_fact,
        is_verified=profile.is_verified,
        call_type="onboarding",                  # default; change if needed
        created_at=profile.created_at if profile.created_at else None  # Use provided created_at if available
    )

def chroma_metadata_to_user_profile(metadata: ChromaStudentMetadata) -> UserProfile:
    """
    Converts a ChromaStudentMetadata instance into a UserProfile instance.
    Note: Mapping 'current_location' -> 'location' and 'company_stage' -> 'stage'.
    """
    return UserProfile(
        user_id=metadata.user_id,
        full_name=metadata.full_name,
        university=metadata.university,
        major=metadata.major,
        location=metadata.current_location,      # mapping from Chroma field
        stage=metadata.company_stage,            # mapping from Chroma field
        bio=None,
        most_impressive_fact=metadata.most_impressive_fact,
        linkedin=None,
        github=None,
        website=None,
        twitter=None,
        devpost=None,
        skills=metadata.skills or [],
        interests=metadata.interests or [],
        is_verified=metadata.is_verified,
        created_at=metadata.created_at,
        updated_at=None
    )