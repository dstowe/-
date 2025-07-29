# personal_config.py - COMPLETE VERSION WITH ALL METHODS
"""
Personal Trading Configuration - SINGLE SOURCE OF TRUTH
This is the ONLY configuration class - completely self-contained
NO inheritance or dependencies on any other config files
ALL configuration parameters are defined here
"""

import os
from datetime import datetime
from typing import List, Dict, Tuple

class PersonalTradingConfig:
    """
    STANDALONE COMPLETE TRADING CONFIGURATION
    This class contains ALL configuration parameters with no dependencies
    This is the ONLY configuration source for the entire trading system
    """

    # =================================================================
    # CORE TRADING PARAMETERS - ALL SELF-CONTAINED
    # =================================================================

    # Database
    DATABASE_PATH = "trading_data.db"

 