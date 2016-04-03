/* A Bison parser, made by GNU Bison 2.3.  */

/* Skeleton interface for Bison's Yacc-like parsers in C

   Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2, or (at your option)
   any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 51 Franklin Street, Fifth Floor,
   Boston, MA 02110-1301, USA.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     ATTACK_TOKEN = 258,
     TRACESTEP_TOKEN = 259,
     BECAUSE_TOKEN = 260,
     ATOM = 261,
     QUOTE = 262,
     SP = 263,
     END_LINE = 264,
     PRIMITIVE = 265,
     DERIVED = 266,
     META = 267,
     METRIC = 268,
     DESC = 269,
     FLOAT = 270,
     CVSS_AC = 271,
     CAP_LUCK = 272
   };
#endif
/* Tokens.  */
#define ATTACK_TOKEN 258
#define TRACESTEP_TOKEN 259
#define BECAUSE_TOKEN 260
#define ATOM 261
#define QUOTE 262
#define SP 263
#define END_LINE 264
#define PRIMITIVE 265
#define DERIVED 266
#define META 267
#define METRIC 268
#define DESC 269
#define FLOAT 270
#define CVSS_AC 271
#define CAP_LUCK 272




#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef int YYSTYPE;
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
# define YYSTYPE_IS_TRIVIAL 1
#endif

extern YYSTYPE yylval;

