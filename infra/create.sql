CREATE TABLE
    prices (
        id BIGSERIAL PRIMARY KEY,  -- Use BIGSERIAL for larger auto-increment range
        name VARCHAR(255),
        category VARCHAR(255),
        price VARCHAR(255),
        link VARCHAR(255),
        last_discount VARCHAR(255),
        last_update VARCHAR(255),
        store VARCHAR(255)
    );