
import logging
import sys
import traceback

class MainSystem:
    """
    Enhanced Automated Multi-Account Trading System - REFACTORED
    Now uses PersonalTradingConfig as the SINGLE SOURCE OF TRUTH for ALL configuration
    No competing configuration logic - everything defers to PersonalTradingConfig
    """
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def authenticate(self) -> bool:
        """Handle authentication using the new modular system"""
        try:
            self.logger.info("🔐 Step: Authentication")
            
            # Try to load existing session first
            if self.session_manager.auto_manage_session(self.wb):
                self.logger.info("✅ Using existing session")
                # Verify login status and ensure account context is properly initialized
                if self.login_manager.check_login_status():
                    self.is_logged_in = True
                    return True
                else:
                    self.logger.warning("Session loaded but login verification failed")
                    # Clear potentially bad session and try fresh login
                    self.session_manager.clear_session()
            
            # If no valid session or verification failed, perform fresh login
            self.logger.info("Attempting fresh login...")
            if self.login_manager.login_automatically():
                self.logger.info("✅ Fresh login successful")
                self.is_logged_in = True 

      
                # Save the new session
                self.session_manager.save_session(self.wb)
                return True
            else:
                self.logger.error("❌ CRITICAL: Authentication failed after all retries")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Authentication error: {e}")
            return False






def main():
    """Main entry point for enhanced automated system - REFACTORED with PersonalTradingConfig as SINGLE SOURCE OF TRUTH"""
    try:
        system = MainSystem()
        success = system.authenticate()

        print(success)
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
        
    except Exception as e:
        logging.error(f"Critical enhanced system error: {e}")
        logging.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
        main()