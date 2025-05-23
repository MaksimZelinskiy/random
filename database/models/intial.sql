
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    username VARCHAR(255) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    lang VARCHAR(255) NULL,
    referrer_id VARCHAR(255) NULL DEFAULT 'search', 
    date_reg TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_login (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,    
    data JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_mailings (
    id SERIAL PRIMARY KEY,  
    created_by_admin_id BIGINT NOT NULL,            
    task_type VARCHAR(255) NOT NULL,
    target_id VARCHAR(255) NOT NULL,
    message_type VARCHAR(255) NOT NULL,
    media_file_id VARCHAR(255) NULL,
    text TEXT NULL,
    reply_markup JSONB NOT NULL,
    scheduled_at TIMESTAMP NOT NULL,
    sent_at TIMESTAMP NULL,
    status VARCHAR(255) NOT NULL DEFAULT 'pending',
    retry_count INT NOT NULL DEFAULT 0,
    error_message TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);  

CREATE TABLE giveaways (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    admin_id INT NOT NULL,
    publish_channels JSONB NOT NULL,
    required_channels JSONB NOT NULL,
    view_details JSONB NOT NULL,    
    count_participants INT NOT NULL DEFAULT 0,
    count_winners INT NOT NULL DEFAULT 0,
    use_boost BOOLEAN NOT NULL DEFAULT FALSE,
    use_capha BOOLEAN NOT NULL DEFAULT FALSE,
    use_block_twinks BOOLEAN NOT NULL DEFAULT FALSE,
    start_at TIMESTAMP NOT NULL,
    ends_at TIMESTAMP NOT NULL, 
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    status VARCHAR(255) NOT NULL DEFAULT 'active',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);  

CREATE TABLE giveaway_participants (        
    id SERIAL PRIMARY KEY,
    giveaway_id INT NOT NULL,
    user_id INT NOT NULL,
    user_ip VARCHAR(255) NOT NULL,
    count_boost INT NOT NULL DEFAULT 0,
    status VARCHAR(255) NOT NULL,
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE giveaway_winners (
    id SERIAL PRIMARY KEY,
    giveaway_id INT NOT NULL,
    user_id INT NOT NULL,
    place INT NOT NULL,
    type VARCHAR(255) NOT NULL,
    selected_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);              

CREATE TABLE user_admin_bind (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    admin_id INT NOT NULL,
    giveaway_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);  

CREATE TABLE admin_channel_bind (
    id SERIAL PRIMARY KEY,
    admin_id INT NOT NULL,
    channel_id INT NOT NULL,
    channel_title VARCHAR(255) NOT NULL,
    channels_username VARCHAR(255) NOT NULL,
    channels_link VARCHAR(255) NOT NULL,
    channel_status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);  

CREATE TABLE user_subscription (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    giveaway_id VARCHAR(255) NOT NULL,
    channel_id INT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
); 

     
