#!/usr/bin/env python3
"""
Enhanced Automated Multi-Account Trading System - FIXED MAIN.PY
Handles authentication, account discovery, and comprehensive logging
"""

import logging
import sys
import traceback
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict

# Import our modules
from webull.webull import webull
from auth.credentials import CredentialManager
from auth.login_manager import LoginManager
from auth.session_manager import SessionManager
from accounts.account_manager import AccountManager
from config.config import PersonalTradingConfig

class MainSystem:
    """
    Enhanced Automated Multi-Account Trading System - COMPLETE IMPLEMENTATION
    Handles authentication, account discovery, and logging to /logs directory
    """
    
    def __init__(self):
        # Initialize all attributes first
        self.logger = None
        self.wb = None
        self.config = None
        self.credential_manager = None
        self.login_manager = None
        self.session_manager = None
        self.account_manager = None
        self.is_logged_in = False
        
        # Set up logging first
        self.setup_logging()
        
        # Initialize the system
        self._initialize_system()
    
    def setup_logging(self):
        """Set up comprehensive logging to /logs directory"""
        try:
            # Create logs directory if it doesn't exist
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)
            
            # Create timestamped log filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_filename = logs_dir / f"trading_system_{timestamp}.log"
            
            # Configure root logger
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                handlers=[
                    logging.FileHandler(log_filename, encoding='utf-8'),
                    logging.StreamHandler(sys.stdout)  # Also log to console
                ],
                force=True  # Force reconfiguration
            )
            
            # Create logger for this module
            self.logger = logging.getLogger(__name__)
            self.logger.info("="*80)
            self.logger.info("🚀 ENHANCED MULTI-ACCOUNT TRADING SYSTEM STARTING")
            self.logger.info("="*80)
            self.logger.info(f"📝 Logging to: {log_filename}")
            self.logger.info(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
        except Exception as e:
            print(f"❌ CRITICAL: Failed to setup logging: {e}")
            print(traceback.format_exc())
            sys.exit(1)
    
    def _initialize_system(self):
        """Initialize all system components"""
        try:
            self.logger.info("🔧 Initializing system components...")
            
            # Initialize configuration
            self.logger.debug("Loading PersonalTradingConfig...")
            self.config = PersonalTradingConfig()
            self.logger.info("✅ Configuration loaded")
            
            # Initialize Webull client
            self.logger.debug("Initializing Webull client...")
            self.wb = webull()
            self.logger.info("✅ Webull client initialized")
            
            # Initialize authentication components
            self.logger.debug("Initializing authentication components...")
            self.credential_manager = CredentialManager(logger=self.logger)
            self.login_manager = LoginManager(self.wb, self.credential_manager, logger=self.logger)
            self.session_manager = SessionManager(logger=self.logger)
            self.logger.info("✅ Authentication components initialized")
            
            # Initialize account manager
            self.logger.debug("Initializing account manager...")
            self.account_manager = AccountManager(self.wb, self.config, logger=self.logger)
            self.logger.info("✅ Account manager initialized")
            
            self.logger.info("🎯 All system components initialized successfully")
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ CRITICAL: Failed to initialize system components: {e}")
                self.logger.error(traceback.format_exc())
            else:
                print(f"❌ CRITICAL: Failed to initialize system components: {e}")
                print(traceback.format_exc())
            raise
    
    def authenticate(self) -> bool:
        """Handle authentication using the modular authentication system"""
        try:
            self.logger.info("🔐 Step 1: Authentication Process Starting")
            self.logger.info("-" * 60)
            
            # Check if credentials exist
            if not self.credential_manager.credentials_exist():
                self.logger.error("❌ No encrypted credentials found!")
                self.logger.info("💡 Please run credential setup first:")
                self.logger.info("   python -c \"from auth.credentials import setup_credentials_interactive; setup_credentials_interactive()\"")
                self.logger.info("💡 If you get image verification errors, add a browser DID:")
                self.logger.info("   python add_did.py")
                return False
            
            # Load credentials and set DID automatically
            credentials = self.credential_manager.load_credentials()
            stored_did = credentials.get('did')
            
            if stored_did:
                self.logger.info(f"✅ Setting DID from credentials: {stored_did[:8]}...{stored_did[-8:]}")
                self.wb._set_did(stored_did)
                
                # Also save to did.bin for consistency
                try:
                    import pickle
                    with open('did.bin', 'wb') as f:
                        pickle.dump(stored_did, f)
                    self.logger.debug("✅ did.bin file updated")
                except Exception as e:
                    self.logger.debug(f"⚠️ Could not update did.bin: {e}")
            else:
                self.logger.warning("⚠️ No DID stored in credentials - this may cause image verification errors")
                self.logger.warning("💡 To fix this, you need to add a browser DID to your credentials:")
                self.logger.warning("   1. Open Webull in browser and log in")
                self.logger.warning("   2. Get DID from browser (F12 → Network → Headers → 'did' field)")
                self.logger.warning("   3. Run: python add_did.py")
                self.logger.info("🔄 Continuing with auto-generated DID...")
            
            # Try to load existing session first
            self.logger.info("🔍 Checking for existing session...")
            if self.session_manager.auto_manage_session(self.wb):
                self.logger.info("✅ Existing session loaded successfully")
                
                # Verify login status and ensure account context is properly initialized
                if self.login_manager.check_login_status():
                    self.logger.info("✅ Session verified and account context initialized")
                    self.is_logged_in = True
                    return True
                else:
                    self.logger.warning("⚠️ Session loaded but login verification failed")
                    self.logger.info("🧹 Clearing potentially bad session...")
                    self.session_manager.clear_session()
            else:
                self.logger.info("ℹ️ No valid existing session found")
            
            # Perform fresh login with retry logic
            max_attempts = 3
            for attempt in range(1, max_attempts + 1):
                self.logger.info(f"🔑 Login attempt {attempt}/{max_attempts}")
                
                if self.login_manager.login_automatically():
                    self.logger.info("✅ Fresh authentication successful!")
                    self.is_logged_in = True
                    
                    # Save the new session for future use
                    self.logger.info("💾 Saving session for future use...")
                    if self.session_manager.save_session(self.wb):
                        self.logger.info("✅ Session saved successfully")
                    else:
                        self.logger.warning("⚠️ Session save failed (non-critical)")
                    
                    return True
                else:
                    self.logger.error(f"❌ Login attempt {attempt} failed")
                    
                    if attempt < max_attempts:
                        self.logger.info("⏳ Waiting 30 seconds before retry...")
                        time.sleep(30)
                    else:
                        self.logger.error("❌ All login attempts failed")
                        if not stored_did:
                            self.logger.error("💡 SOLUTION: Add a browser DID to your credentials:")
                            self.logger.error("   python add_did.py")
                        
            return False
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Authentication error: {e}")
                self.logger.error(traceback.format_exc())
            else:
                print(f"❌ Authentication error: {e}")
                print(traceback.format_exc())
            return False
    
    def discover_accounts(self) -> bool:
        """Discover and load all available trading accounts"""
        try:
            self.logger.info("🔍 Step 2: Account Discovery Process Starting")
            self.logger.info("-" * 60)
            
            if not self.is_logged_in:
                self.logger.error("❌ Cannot discover accounts - not authenticated")
                return False
            
            # Discover all accounts
            self.logger.info("🔍 Discovering all available accounts...")
            if self.account_manager.discover_accounts():
                self.logger.info("✅ Account discovery completed successfully")
                
                # Get account summary
                summary = self.account_manager.get_account_summary()
                self.logger.info("📊 Account Discovery Summary:")
                self.logger.info(f"   Total Accounts Found: {summary['total_accounts']}")
                self.logger.info(f"   Enabled for Trading: {summary['enabled_accounts']}")
                self.logger.info(f"   Total Portfolio Value: ${summary['total_value']:,.2f}")
                self.logger.info(f"   Total Available Cash: ${summary['total_cash']:,.2f}")
                self.logger.info(f"   Total Positions: {summary['total_positions']}")
                
                # Log detailed account information
                self.logger.info("\n📋 Detailed Account Information:")
                for i, account_info in enumerate(summary['accounts'], 1):
                    self.logger.info(f"   Account {i}:")
                    self.logger.info(f"      Type: {account_info['account_type']}")
                    self.logger.info(f"      ID: {account_info['account_id']}")
                    self.logger.info(f"      Enabled: {'✅ Yes' if account_info['enabled'] else '❌ No'}")
                    self.logger.info(f"      Net Liquidation: ${account_info['net_liquidation']:,.2f}")
                    self.logger.info(f"      Available Funds: ${account_info['settled_funds']:,.2f}")
                    self.logger.info(f"      Positions: {account_info['positions_count']}")
                    self.logger.info(f"      Day Trading: {'✅ Enabled' if account_info['day_trading_enabled'] else '❌ Disabled'}")
                    self.logger.info(f"      Options Trading: {'✅ Enabled' if account_info['options_enabled'] else '❌ Disabled'}")
                    
                    if i < len(summary['accounts']):
                        self.logger.info("")
                
                # Log enabled accounts specifically
                enabled_accounts = self.account_manager.get_enabled_accounts()
                if enabled_accounts:
                    self.logger.info("🎯 Accounts Enabled for Trading:")
                    for account in enabled_accounts:
                        self.logger.info(f"   ✅ {account.account_type}: ${account.settled_funds:,.2f} available")
                else:
                    self.logger.warning("⚠️ No accounts are currently enabled for trading!")
                    self.logger.info("💡 Check your PersonalTradingConfig ACCOUNT_CONFIGURATIONS")
                
                return True
            else:
                self.logger.error("❌ Account discovery failed")
                return False
                
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Account discovery error: {e}")
                self.logger.error(traceback.format_exc())
            else:
                print(f"❌ Account discovery error: {e}")
                print(traceback.format_exc())
            return False
    
    def log_system_status(self):
        """Log comprehensive system status"""
        try:
            self.logger.info("📊 Step 3: System Status Report")
            self.logger.info("-" * 60)
            
            # Authentication status
            login_info = self.login_manager.get_login_info()
            self.logger.info("🔐 Authentication Status:")
            self.logger.info(f"   Logged In: {'✅ Yes' if login_info['is_logged_in'] else '❌ No'}")
            self.logger.info(f"   Access Token: {'✅ Present' if login_info['access_token_exists'] else '❌ Missing'}")
            self.logger.info(f"   Trade Token: {'✅ Present' if login_info['trade_token_exists'] else '❌ Missing'}")
            self.logger.info(f"   Account ID: {login_info['account_id'] or 'Not Set'}")
            
            # Session status
            session_info = self.session_manager.get_session_info()
            self.logger.info("💾 Session Status:")
            self.logger.info(f"   Session Exists: {'✅ Yes' if session_info['exists'] else '❌ No'}")
            if session_info['exists']:
                self.logger.info(f"   Saved At: {session_info['saved_at']}")
                if session_info.get('expires_in_minutes') is not None:
                    self.logger.info(f"   Expires In: {session_info['expires_in_minutes']} minutes")
            
            # Configuration status
            self.logger.info("⚙️ Configuration Status:")
            self.logger.info(f"   Config Loaded: {'✅ Yes' if self.config else '❌ No'}")
            if hasattr(self.config, 'DATABASE_PATH'):
                self.logger.info(f"   Database Path: {self.config.DATABASE_PATH}")
            
            # Account status
            if hasattr(self, 'account_manager') and self.account_manager.accounts:
                self.logger.info("👥 Account Manager Status:")
                self.logger.info(f"   Accounts Loaded: {len(self.account_manager.accounts)}")
                self.logger.info(f"   Current Account: {self.account_manager.current_account.account_type if self.account_manager.current_account else 'None'}")
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ Error generating system status: {e}")
            else:
                print(f"❌ Error generating system status: {e}")
    
    def run(self) -> bool:
        """Run the complete system workflow"""
        try:
            self.logger.info("🚀 Starting Enhanced Multi-Account Trading System Workflow")
            self.logger.info("=" * 80)
            
            # Step 1: Authentication
            if not self.authenticate():
                self.logger.error("❌ Authentication failed - cannot continue")
                return False
            
            # Step 2: Account Discovery
            if not self.discover_accounts():
                self.logger.error("❌ Account discovery failed - cannot continue")
                return False
            
            # Step 3: System Status Report
            self.log_system_status()
            
            # Success summary
            self.logger.info("=" * 80)
            self.logger.info("🎉 SYSTEM INITIALIZATION COMPLETED SUCCESSFULLY!")
            self.logger.info("=" * 80)
            self.logger.info("✅ Authentication: Complete")
            self.logger.info("✅ Account Discovery: Complete")
            self.logger.info("✅ System Status: Logged")
            self.logger.info("🚀 System is ready for trading operations")
            
            return True
            
        except Exception as e:
            if self.logger:
                self.logger.error(f"❌ CRITICAL: System workflow failed: {e}")
                self.logger.error(traceback.format_exc())
            else:
                print(f"❌ CRITICAL: System workflow failed: {e}")
                print(traceback.format_exc())
            return False
        finally:
            # Always log completion
            if self.logger:
                self.logger.info("=" * 80)
                self.logger.info(f"⏰ System workflow completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                self.logger.info("=" * 80)
    
    def cleanup(self):
        """Clean up system resources"""
        try:
            if self.logger:
                self.logger.info("🧹 Cleaning up system resources...")
            
            # Restore original account context if needed
            if self.account_manager:
                self.account_manager.restore_original_account()
            
            # Logout if needed
            if self.login_manager and self.is_logged_in:
                self.login_manager.logout()
            
            if self.logger:
                self.logger.info("✅ Cleanup completed")
            
        except Exception as e:
            if self.logger:
                self.logger.warning(f"⚠️ Cleanup warning: {e}")
            else:
                print(f"⚠️ Cleanup warning: {e}")


def main():
    """Main entry point for enhanced automated system"""
    system = None
    success = False
    
    try:
        # Initialize and run the system
        system = MainSystem()
        success = system.run()
        
        # Exit with appropriate code
        if success:
            print(f"\n🎉 System completed successfully! Check logs in /logs directory")
            sys.exit(0)
        else:
            print(f"\n❌ System failed! Check logs in /logs directory for details")
            sys.exit(1)
        
    except KeyboardInterrupt:
        if system and system.logger:
            system.logger.info("🛑 System interrupted by user (Ctrl+C)")
        else:
            print("\n🛑 System interrupted by user (Ctrl+C)")
        sys.exit(1)
        
    except Exception as e:
        if system and system.logger:
            system.logger.error(f"❌ CRITICAL: Unexpected system error: {e}")
            system.logger.error(traceback.format_exc())
        else:
            print(f"❌ CRITICAL: Unexpected system error: {e}")
            print(traceback.format_exc())
        sys.exit(1)
        
    finally:
        # Always attempt cleanup
        if system:
            system.cleanup()


if __name__ == "__main__":
    main()