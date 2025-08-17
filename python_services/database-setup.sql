-- PhishGuard Database Schema
-- PostgreSQL with pgvector extension for AI/ML integration

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgvector";

-- Users table for authentication and user management
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('user', 'moderator', 'admin')),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    preferences JSONB DEFAULT '{}'
);

-- Scam URLs table (enhanced for AI training)
CREATE TABLE scam_urls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    url_hash VARCHAR(64) UNIQUE NOT NULL,
    original_url TEXT NOT NULL,
    domain VARCHAR(255) NOT NULL,
    threat_type VARCHAR(100) NOT NULL,
    confidence DECIMAL(3,2) DEFAULT 0.8,
    source VARCHAR(100) NOT NULL,
    tags TEXT[],
    metadata JSONB DEFAULT '{}',
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    report_count INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,
    ai_confidence DECIMAL(3,2),
    ml_features JSONB DEFAULT '{}',
    embedding vector(1536) -- For OpenAI embeddings
);

-- User reports table
CREATE TABLE user_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    url_hash VARCHAR(64) NOT NULL,
    original_url TEXT NOT NULL,
    description TEXT,
    report_type VARCHAR(50) DEFAULT 'scam',
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'approved', 'rejected')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    reviewed_by UUID REFERENCES users(id),
    ai_analysis JSONB DEFAULT '{}',
    user_metadata JSONB DEFAULT '{}'
);

-- Detection history for AI training data
CREATE TABLE detection_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    url_hash VARCHAR(64) NOT NULL,
    original_url TEXT NOT NULL,
    threat_level VARCHAR(50) NOT NULL,
    confidence DECIMAL(3,2) NOT NULL,
    detection_methods TEXT[],
    is_suspicious BOOLEAN NOT NULL,
    response_time_ms INTEGER,
    user_agent TEXT,
    ip_address INET,
    session_id VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ai_prediction JSONB DEFAULT '{}'
);

-- AI Model Training Data
CREATE TABLE ai_training_data (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    url_hash VARCHAR(64) NOT NULL,
    original_url TEXT NOT NULL,
    content_text TEXT,
    html_content TEXT,
    screenshot_path VARCHAR(500),
    features JSONB NOT NULL,
    label VARCHAR(50) NOT NULL,
    confidence DECIMAL(3,2),
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified BOOLEAN DEFAULT false,
    verified_by UUID REFERENCES users(id)
);

-- Vector embeddings for RAG system
CREATE TABLE knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    content_type VARCHAR(50) NOT NULL, -- 'safety_tip', 'scam_pattern', 'recovery_guide'
    embedding vector(1536),
    tags TEXT[],
    language VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT true,
    metadata JSONB DEFAULT '{}'
);

-- Chat sessions for chatbot training
CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    total_messages INTEGER DEFAULT 0,
    session_data JSONB DEFAULT '{}'
);

-- Chat messages for training data
CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(100) NOT NULL,
    message_type VARCHAR(20) NOT NULL CHECK (message_type IN ('user', 'bot', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    intent VARCHAR(100),
    confidence DECIMAL(3,2),
    entities JSONB DEFAULT '{}',
    response_time_ms INTEGER,
    user_satisfaction INTEGER CHECK (user_satisfaction >= 1 AND user_satisfaction <= 5)
);

-- API status tracking
CREATE TABLE api_status (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    api_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    response_time_ms INTEGER,
    success_rate DECIMAL(5,2),
    daily_requests INTEGER DEFAULT 0
);

-- Model performance metrics
CREATE TABLE model_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL,
    metric_type VARCHAR(50) NOT NULL, -- 'accuracy', 'precision', 'recall', 'f1'
    metric_value DECIMAL(5,4) NOT NULL,
    dataset_size INTEGER,
    training_duration_minutes INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

-- Create indexes for performance
CREATE INDEX idx_scam_urls_hash ON scam_urls(url_hash);
CREATE INDEX idx_scam_urls_domain ON scam_urls(domain);
CREATE INDEX idx_scam_urls_active ON scam_urls(is_active);
CREATE INDEX idx_scam_urls_embedding ON scam_urls USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_detection_history_url ON detection_history(url_hash);
CREATE INDEX idx_detection_history_time ON detection_history(timestamp);
CREATE INDEX idx_user_reports_status ON user_reports(status);
CREATE INDEX idx_knowledge_base_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_chat_messages_session ON chat_messages(session_id);
CREATE INDEX idx_chat_messages_time ON chat_messages(timestamp);

-- Create GIN indexes for JSONB fields
CREATE INDEX idx_scam_urls_metadata ON scam_urls USING GIN (metadata);
CREATE INDEX idx_user_reports_ai_analysis ON user_reports USING GIN (ai_analysis);
CREATE INDEX idx_detection_history_ai_prediction ON detection_history USING GIN (ai_prediction);
CREATE INDEX idx_ai_training_data_features ON ai_training_data USING GIN (features);

-- Create full-text search indexes
CREATE INDEX idx_knowledge_base_content_fts ON knowledge_base USING GIN (to_tsvector('english', content));
CREATE INDEX idx_scam_urls_description_fts ON user_reports USING GIN (to_tsvector('english', description));

-- Insert default knowledge base content for RAG
INSERT INTO knowledge_base (title, content, content_type, tags, language) VALUES
('How to Spot Phishing Links', 'Phishing links often have suspicious domains, urgent language, and ask for personal information. Always check the URL carefully before clicking.', 'safety_tip', ARRAY['phishing', 'security', 'links'], 'en'),
('Myanmar Bank Scam Warning', 'Scammers often impersonate KBZ Bank, Ayeyarwady Bank, and other Myanmar banks. Never enter your banking details on suspicious links.', 'scam_pattern', ARRAY['myanmar', 'bank', 'kbz', 'scam'], 'en'),
('Account Recovery Steps', 'If you clicked a suspicious link: 1) Change passwords immediately 2) Enable 2FA 3) Contact your bank 4) Report to authorities', 'recovery_guide', ARRAY['recovery', 'security', 'emergency'], 'en'),
('Lottery Scam Detection', 'Fake lottery scams promise large prizes but ask for fees or personal information. Real lotteries never ask for money upfront.', 'scam_pattern', ARRAY['lottery', 'scam', 'money'], 'en'),
('Investment Scam Warning', 'Be wary of investment opportunities promising high returns with little risk. These are often Ponzi schemes or frauds.', 'scam_pattern', ARRAY['investment', 'scam', 'money'], 'en');

-- Create views for common queries
CREATE VIEW recent_scams AS
SELECT 
    original_url,
    domain,
    threat_type,
    confidence,
    report_count,
    first_seen,
    last_seen
FROM scam_urls 
WHERE is_active = true 
ORDER BY last_seen DESC;

CREATE VIEW detection_stats AS
SELECT 
    DATE(timestamp) as date,
    COUNT(*) as total_detections,
    COUNT(CASE WHEN is_suspicious = true THEN 1 END) as suspicious_count,
    AVG(confidence) as avg_confidence,
    AVG(response_time_ms) as avg_response_time
FROM detection_history 
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- Create functions for common operations
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_scam_urls_updated_at BEFORE UPDATE ON scam_urls FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ai_training_data_updated_at BEFORE UPDATE ON ai_training_data FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_knowledge_base_updated_at BEFORE UPDATE ON knowledge_base FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to find similar content using vector search
CREATE OR REPLACE FUNCTION find_similar_content(query_embedding vector(1536), similarity_threshold float DEFAULT 0.7)
RETURNS TABLE (
    id UUID,
    title VARCHAR(255),
    content TEXT,
    content_type VARCHAR(50),
    similarity float
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        kb.id,
        kb.title,
        kb.content,
        kb.content_type,
        1 - (kb.embedding <=> query_embedding) as similarity
    FROM knowledge_base kb
    WHERE kb.is_active = true 
    AND 1 - (kb.embedding <=> query_embedding) > similarity_threshold
    ORDER BY kb.embedding <=> query_embedding;
END;
$$ LANGUAGE plpgsql; 