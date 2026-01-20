ALTER TABLE "account" ADD COLUMN "account_id" text NOT NULL;--> statement-breakpoint
CREATE INDEX "account_account_id_idx" ON "account" USING btree ("account_id");