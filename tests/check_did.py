#!/usr/bin/env python3
"""
Check and Update Stored DID in Encrypted Credentials
This script will show you what DID is currently stored and allow you to update it
"""

import os
from ..auth import CredentialManager

def check_and_manage_did():
    """Check current DID and optionally update it"""
    print("🔍 CHECKING STORED DID IN CREDENTIALS")
    print("=" * 50)
    
    # Initialize credential manager
    cred_manager = CredentialManager()
    
    # Check if credentials exist
    if not cred_manager.credentials_exist():
        print("❌ No encrypted credentials found!")
        print("💡 Please run credential setup first:")
        print("   python -c \"from auth.credentials import setup_credentials_interactive; setup_credentials_interactive()\"")
        return False
    
    try:
        # Load current credentials
        credentials = cred_manager.load_credentials()
        current_did = credentials.get('did')
        
        print("📋 Current Credential Status:")
        print(f"   Username: {credentials.get('username', 'Not found')}")
        print(f"   Password: {'***' if credentials.get('password') else 'Not found'}")
        print(f"   Trading PIN: {'***' if credentials.get('trading_pin') else 'Not found'}")
        print(f"   DID: {current_did if current_did else 'Not stored'}")
        print(f"   Created: {credentials.get('created_date', 'Unknown')}")
        print()
        
        # Check if did.bin exists (Webull's default DID storage)
        did_bin_exists = os.path.exists('did.bin')
        print(f"📁 did.bin file exists: {'✅ Yes' if did_bin_exists else '❌ No'}")
        
        if did_bin_exists:
            try:
                import pickle
                with open('did.bin', 'rb') as f:
                    file_did = pickle.load(f)
                print(f"   DID in did.bin: {file_did}")
                
                # Compare DIDs
                if current_did and current_did != file_did:
                    print("⚠️  WARNING: DIDs don't match!")
                    print(f"   Credentials DID: {current_did}")
                    print(f"   did.bin DID: {file_did}")
                elif current_did == file_did:
                    print("✅ DIDs match - good!")
                    
            except Exception as e:
                print(f"❌ Error reading did.bin: {e}")
        
        print()
        
        # Options for user
        if not current_did:
            print("🔧 No DID stored in credentials.")
            print("Options:")
            print("1. Enter a browser DID (recommended)")
            print("2. Use auto-generated DID (may cause image verification)")
            print("3. Exit")
            
            choice = input("Choose option (1-3): ").strip()
            
            if choice == "1":
                return update_did_in_credentials(cred_manager, credentials)
            elif choice == "2":
                print("💡 Auto-generated DID will be used (may require image verification)")
                return True
            else:
                print("👋 Exiting")
                return False
                
        else:
            print("🔧 DID found in credentials.")
            print("If you're still getting image verification errors, the stored DID may be invalid.")
            print("Options:")
            print("1. Try using current DID")
            print("2. Update DID with browser DID")
            print("3. Exit")
            
            choice = input("Choose option (1-3): ").strip()
            
            if choice == "1":
                print("✅ Will try using current stored DID")
                return True
            elif choice == "2":
                return update_did_in_credentials(cred_manager, credentials)
            else:
                print("👋 Exiting")
                return False
                
    except Exception as e:
        print(f"❌ Error checking credentials: {e}")
        return False

def update_did_in_credentials(cred_manager, current_credentials):
    """Update the DID in encrypted credentials"""
    print()
    print("🖥️  GET DID FROM BROWSER:")
    print("1. Open Webull in your browser and log in")
    print("2. Open Developer Tools (F12)")
    print("3. Go to Network tab")
    print("4. Refresh the page")
    print("5. Look at any request's headers")
    print("6. Find the 'did' header (32-character hex string)")
    print()
    
    new_did = input("Enter your browser DID: ").strip()
    
    if not new_did:
        print("❌ No DID provided")
        return False
    
    if len(new_did) != 32:
        print(f"⚠️  Warning: DID should be 32 characters, got {len(new_did)}")
        confirm = input("Continue anyway? (y/n): ").lower().strip()
        if confirm not in ['y', 'yes']:
            return False
    
    try:
        # Update credentials with new DID
        success = cred_manager.update_credentials(did=new_did)
        
        if success:
            print(f"✅ DID updated successfully in credentials!")
            print(f"   New DID: {new_did}")
            
            # Also update did.bin file for consistency
            try:
                import pickle
                with open('did.bin', 'wb') as f:
                    pickle.dump(new_did, f)
                print("✅ did.bin file also updated")
            except Exception as e:
                print(f"⚠️  Warning: Could not update did.bin: {e}")
            
            print()
            print("🚀 You can now run the main system:")
            print("   python main.py")
            return True
        else:
            print("❌ Failed to update credentials")
            return False
            
    except Exception as e:
        print(f"❌ Error updating DID: {e}")
        return False

def quick_did_check():
    """Quick check of DID status"""
    cred_manager = CredentialManager()
    
    if not cred_manager.credentials_exist():
        return "❌ No credentials found"
    
    try:
        credentials = cred_manager.load_credentials()
        did = credentials.get('did')
        
        if did:
            return f"✅ DID stored: {did[:8]}...{did[-8:]}"  # Show first and last 8 chars
        else:
            return "⚠️  No DID in credentials"
            
    except Exception as e:
        return f"❌ Error: {e}"

if __name__ == "__main__":
    try:
        print("🔍 Quick DID Status:", quick_did_check())
        print()
        
        success = check_and_manage_did()
        if success:
            print("\n✅ Ready to run main system!")
        else:
            print("\n❌ Please resolve DID issues before running main system")
            
    except KeyboardInterrupt:
        print("\n🛑 Cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")