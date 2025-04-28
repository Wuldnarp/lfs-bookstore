CREATE TABLE IF NOT EXISTS [User] (
  [username] TEXT,
  [password] TEXT,
  PRIMARY KEY ([username])
);

CREATE TABLE IF NOT EXISTS [Book] (
  [ID] TEXT,
  [UserID] TEXT,
  [Title] TEXT,
  PRIMARY KEY ([ID]),
  FOREIGN KEY ([UserID]) REFERENCES [User]([username])
);

CREATE TABLE IF NOT EXISTS [Transaction] (
  [ID] TEXT,
  [SellerID] TEXT,
  [BuyerID] TEXT,
  [BookID] TEXT,
  [Price] INTEGER,
  [Date] TEXT,
  PRIMARY KEY ([ID]),
  FOREIGN KEY ([SellerID]) REFERENCES [User]([username]),
  FOREIGN KEY ([BuyerID]) REFERENCES [User]([username]),
  FOREIGN KEY ([BookID]) REFERENCES [Book]([ID])
);
