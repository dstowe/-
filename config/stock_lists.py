# config/stock_lists.py - IMPROVED VERSION
"""
Stock Lists Configuration - Optimized and Clean
Centralized stock symbol management for different trading strategies
"""

from typing import List, Dict, Set, Optional
from datetime import datetime
import logging

class StockLists:
    """
    Optimized stock lists with validation, deduplication, and better organization
    """
    
    # =================================================================
    # CORE STRATEGY LISTS - OPTIMIZED AND VALIDATED
    # =================================================================
    
    # Core ETFs - High liquidity foundation (reduced from 100+ to focused set)
    CORE_ETFS = [
        'SPY', 'QQQ', 'IWM',  # Market indexes
        'VTV', 'VUG', 'IWD', 'IWF',  # Style factors
        'XLF', 'XLE', 'XLV', 'XLI', 'XLU', 'XLP', 'XLRE',  # Sectors
        'VEA', 'VWO',  # International
    ]
    
    # Mean reversion optimized for 2025 market (reduced and focused)
    MEAN_REVERSION = [
        # Core ETFs for liquidity and clean signals
        *CORE_ETFS,
        
        # Mega Cap Tech - High volume, optimal volatility
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META',
        
        # Financials - Rate environment beneficiaries
        'JPM', 'BAC', 'USB', 'TFC', 'PNC', 'WFC', 'GS', 'MS',
        
        # Energy Value - Strong BB patterns
        'XOM', 'CVX', 'EOG', 'COP',
        
        # Defensive Value - Dividend aristocrats
        'JNJ', 'PG', 'KO', 'UNH', 'HD', 'MCD',
        
        # REITs - Undervalued sector
        'O', 'PLD', 'CCI', 'AMT',
        
        # Utilities - Low volatility boundaries
        'DUK', 'SO', 'NEE',
    ]
    
    # Sector rotation - All major sectors
    SECTOR_ROTATION = [
        'XLK',   # Technology
        'XLF',   # Financials  
        'XLE',   # Energy
        'XLV',   # Healthcare
        'XLI',   # Industrials
        'XLP',   # Consumer Staples
        'XLU',   # Utilities
        'XLY',   # Consumer Discretionary
        'XLB',   # Materials
        'XLRE',  # Real Estate
        'XLC',   # Communication Services
    ]
    
    # International exposure
    INTERNATIONAL_OUTPERFORMANCE = [
        # Broad international
        'VEA', 'EFA', 'VXUS', 'IEFA',
        # Currency hedged
        'HEFA', 'HEDJ',
        # Regional
        'VGK', 'EWJ', 'VWO', 'EEMA',
        # Country specific
        'EWG', 'EWU', 'EWY', 'INDA', 'FXI',
        # Quality international ADRs
        'ASML', 'NVO', 'TSM', 'UL',
    ]
    
    # Value/rate sensitive universe
    VALUE_RATE_UNIVERSE = [
        # REITs by category
        'PLD', 'EXR',  # Industrial
        'WELL', 'VTR',  # Healthcare
        'SPG', 'REG',   # Retail
        'CCI', 'AMT',   # Infrastructure
        'EQR', 'AVB',   # Residential
        'XLRE', 'IYR',  # REIT ETFs
        
        # Financials by category
        'JPM', 'BAC', 'WFC', 'C',  # Money center
        'USB', 'TFC', 'PNC',       # Regional
        'GS', 'MS',                # Investment banks
        'XLF', 'KBE',              # Financial ETFs
    ]
    
    # High liquidity breakout candidates
    MICROSTRUCTURE_BREAKOUT = [
        # Major ETFs with tightest spreads
        *SECTOR_ROTATION,
        'SPY', 'QQQ', 'IWM', 'VTI', 'VTV', 'VUG',
        
        # Mega cap with best liquidity
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META',
        'BRK.B', 'JNJ', 'JPM', 'V', 'MA', 'UNH',
        
        # High volume growth names
        'AMD', 'NFLX', 'CRM', 'ADBE',
    ]
    
    # Fed policy sensitive
    POLICY_MOMENTUM = [
        # Rate sensitive sectors
        'XLF', 'XLRE', 'XLU',
        
        # Banks (most Fed sensitive)
        'JPM', 'BAC', 'WFC', 'USB', 'TFC',
        
        # Growth stocks (discount rate sensitive)
        'TSLA', 'NVDA', 'AMD', 'CRM', 'NFLX',
        
        # Treasury and volatility ETFs
        'TLT', 'IEF', 'SHY', 'VXX',
        
        # Dollar and commodity sensitivity
        'GLD', 'SLV', 'UUP',
    ]
    
    # Gap trading optimized
    GAP_TRADING = [
        # High volume ETFs
        *CORE_ETFS,
        'ARKK', 'GLD', 'TLT', 'HYG',
        
        # Mega cap tech (high gap frequency)
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META',
        
        # High beta growth
        'AMD', 'SNOW', 'PLTR', 'ROKU', 'ZM',
        
        # Volatile value plays
        'CVS', 'BA', 'X', 'FCX',
    ]
    
    # Bullish momentum
    BULLISH_MOMENTUM = [
        # Momentum leaders
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA',
        
        # Growth tech
        'CRM', 'ADBE', 'NFLX', 'AMD', 'SNOW', 'PLTR',
        
        # Momentum ETFs
        'QQQ', 'ARKK', 'VGT', 'XLK', 'MTUM',
        
        # Sector momentum
        'XLF', 'XLE', 'XLV',
    ]
    
    # =================================================================
    # PORTFOLIO ALLOCATIONS
    # =================================================================
    
    CONSERVATIVE_STRATEGY = [
        'SPY', 'VTV', 'VEA',  # Core (60%)
        'O', 'USB', 'DUK',    # Income (25%)
        'VGK', 'EWJ',         # International (15%)
    ]
    
    AGGRESSIVE_STRATEGY = [
        'QQQ', 'NVDA', 'TSLA', 'AMD',  # Growth (40%)
        *SECTOR_ROTATION[:5],           # Sector rotation (30%)
        'VWO', 'EWY', 'INDA',          # International growth (15%)
        'SPY', 'IWM',                   # Momentum (15%)
    ]
    
    BALANCED_STRATEGY = [
        'SPY', 'QQQ', 'VTV', 'VEA',    # Core (50%)
        'USB', 'O', 'XLF',             # Value/Income (25%)
        'NVDA', 'CRM', 'XLK',          # Growth (15%)
        'VGK', 'VWO',                  # International (10%)
    ]
    
    # =================================================================
    # VALIDATION AND UTILITY METHODS
    # =================================================================
    
    @classmethod
    def validate_symbols(cls, symbol_list: List[str]) -> List[str]:
        """
        Validate and clean symbol list
        - Remove duplicates
        - Check format
        - Log warnings for unusual symbols
        """
        logger = logging.getLogger(__name__)
        
        # Remove duplicates while preserving order
        cleaned_symbols = []
        seen = set()
        
        for symbol in symbol_list:
            if symbol not in seen:
                # Basic validation
                if not symbol or not isinstance(symbol, str):
                    logger.warning(f"Invalid symbol: {symbol}")
                    continue
                    
                # Clean up symbol
                symbol = symbol.strip().upper()
                
                # Check for unusual formats
                if len(symbol) > 6:
                    logger.info(f"Long symbol detected: {symbol}")
                
                cleaned_symbols.append(symbol)
                seen.add(symbol)
        
        return cleaned_symbols
    
    @classmethod
    def get_stocks_for_strategy(cls, strategy_name: str) -> List[str]:
        """Get validated stock list for strategy"""
        
        strategy_mapping = {
            'MeanReversion': cls.MEAN_REVERSION,
            'SectorRotation': cls.SECTOR_ROTATION,
            'International': cls.INTERNATIONAL_OUTPERFORMANCE,
            'ValueRate': cls.VALUE_RATE_UNIVERSE,
            'MicrostructureBreakout': cls.MICROSTRUCTURE_BREAKOUT,
            'PolicyMomentum': cls.POLICY_MOMENTUM,
            'GapTrading': cls.GAP_TRADING,
            'BullishMomentumDip': cls.BULLISH_MOMENTUM,
            'Conservative': cls.CONSERVATIVE_STRATEGY,
            'Aggressive': cls.AGGRESSIVE_STRATEGY,
            'Balanced': cls.BALANCED_STRATEGY,
        }
        
        symbol_list = strategy_mapping.get(strategy_name, cls.MEAN_REVERSION)
        return cls.validate_symbols(symbol_list)
    
    @classmethod
    def get_all_unique_symbols(cls) -> Set[str]:
        """Get all unique symbols across all strategies"""
        all_symbols = set()
        
        # Collect from all major lists
        for attr_name in dir(cls):
            if not attr_name.startswith('_') and attr_name.isupper():
                attr_value = getattr(cls, attr_name)
                if isinstance(attr_value, list):
                    all_symbols.update(attr_value)
        
        return all_symbols
    
    @classmethod
    def get_strategy_info(cls) -> Dict[str, Dict]:
        """Get comprehensive strategy information"""
        return {
            'MeanReversion': {
                'count': len(cls.MEAN_REVERSION),
                'description': 'Optimized mean reversion with focus on 2025 market conditions',
                'market_condition': 'RANGE_BOUND',
                'risk_level': 'Medium',
                'expected_trades_per_week': '3-5'
            },
            'SectorRotation': {
                'count': len(cls.SECTOR_ROTATION),
                'description': 'Systematic sector momentum rotation',
                'market_condition': 'TRENDING',
                'risk_level': 'Medium-High',
                'expected_trades_per_week': '2-3'
            },
            'International': {
                'count': len(cls.INTERNATIONAL_OUTPERFORMANCE),
                'description': 'Global diversification and international opportunities',
                'market_condition': 'ANY',
                'risk_level': 'Medium',
                'expected_trades_per_week': '1-2'
            },
            'ValueRate': {
                'count': len(cls.VALUE_RATE_UNIVERSE),
                'description': 'Rate-sensitive value plays (REITs and financials)',
                'market_condition': 'RATE_ENVIRONMENT',
                'risk_level': 'Medium-Low',
                'expected_trades_per_week': '2-4'
            },
            'GapTrading': {
                'count': len(cls.GAP_TRADING),
                'description': 'High-volume gap reversal opportunities',
                'market_condition': 'HIGH_VOLATILITY',
                'risk_level': 'High',
                'expected_trades_per_week': '5-10'
            }
        }
    
    @classmethod
    def get_symbol_overlap(cls, strategy1: str, strategy2: str) -> Set[str]:
        """Find overlapping symbols between two strategies"""
        list1 = set(cls.get_stocks_for_strategy(strategy1))
        list2 = set(cls.get_stocks_for_strategy(strategy2))
        return list1.intersection(list2)
    
    @classmethod
    def optimize_for_performance(cls, max_symbols_per_strategy: int = 50) -> Dict[str, List[str]]:
        """
        Return performance-optimized versions of strategies
        Reduces list sizes for faster data fetching
        """
        optimized = {}
        
        # Core optimized lists focusing on highest volume/liquidity
        optimized['MeanReversion'] = cls.CORE_ETFS + [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA',
            'JPM', 'BAC', 'XOM', 'CVX', 'JNJ', 'PG', 'O', 'USB'
        ][:max_symbols_per_strategy]
        
        optimized['SectorRotation'] = cls.SECTOR_ROTATION  # Already optimized
        
        optimized['GapTrading'] = cls.CORE_ETFS + [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META',
            'AMD', 'NFLX', 'CRM'
        ][:max_symbols_per_strategy]
        
        return optimized
