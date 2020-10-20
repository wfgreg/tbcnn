PHP_NODE_LIST = [
'Module',
'Expr_VariableSuperGlobal',
'Expr_VariableSuperGlobalUser',
'Comment',
'Comment_Doc',
'Param',
'Scalar_LNumber',
'Scalar_String',
'Scalar_Encapsed',
'Scalar_DNumber',
'Scalar_EncapsedStringPart',
'Scalar_MagicConst_Class',
'Scalar_MagicConst_File',
'Scalar_MagicConst_Namespace',
'Scalar_MagicConst_Trait',
'Scalar_MagicConst_Function',
'Scalar_MagicConst_Line',
'Scalar_MagicConst_Method',
'Scalar_MagicConst_Dir',
'NullableType',
'UnionType',
'Identifier',
'Name_Relative',
'Name_FullyQualified',
'Stmt_Use',
'Stmt_StaticVar',
'Stmt_Class',
'Stmt_Else',
'Stmt_Unset',
'Stmt_ClassConst',
'Stmt_Finally',
'Stmt_TraitUseAdaptation_Alias',
'Stmt_TraitUseAdaptation_Precedence',
'Stmt_Static',
'Stmt_Interface',
'Stmt_Property',
'Stmt_While',
'Stmt_Foreach',
'Stmt_If',
'Stmt_Catch',
'Stmt_Namespace',
'Stmt_Trait',
'Stmt_Function',
'Stmt_Echo',
'Stmt_Nop',
'Stmt_PropertyProperty',
'Stmt_Throw',
'Stmt_GroupUse',
'Stmt_Global',
'Stmt_Continue',
'Stmt_Const',
'Stmt_HaltCompiler',
'Stmt_Do',
'Stmt_InlineHTML',
'Stmt_Break',
'Stmt_TraitUse',
'Stmt_ClassMethod',
'Stmt_Goto',
'Stmt_Expression',
'Stmt_Switch',
'Stmt_TryCatch',
'Stmt_Label',
'Stmt_Return',
'Stmt_Declare',
'Stmt_DeclareDeclare',
'Stmt_UseUse',
'Stmt_Case',
'Stmt_For',
'Stmt_ElseIf',
'Const',
'Name',
'VarLikeIdentifier',
'Expr_UnaryPlus',
'Expr_Array',
'Expr_BinaryOp_Plus',
'Expr_BinaryOp_Smaller',
'Expr_BinaryOp_GreaterOrEqual',
'Expr_BinaryOp_BooleanAnd',
'Expr_BinaryOp_Coalesce',
'Expr_BinaryOp_BitwiseXor',
'Expr_BinaryOp_LogicalAnd',
'Expr_BinaryOp_Pow',
'Expr_BinaryOp_LogicalXor',
'Expr_BinaryOp_BitwiseOr',
'Expr_BinaryOp_SmallerOrEqual',
'Expr_BinaryOp_Mul',
'Expr_BinaryOp_Concat',
'Expr_BinaryOp_Equal',
'Expr_BinaryOp_LogicalOr',
'Expr_BinaryOp_ShiftRight',
'Expr_BinaryOp_BooleanOr',
'Expr_BinaryOp_Identical',
'Expr_BinaryOp_Minus',
'Expr_BinaryOp_ShiftLeft',
'Expr_BinaryOp_BitwiseAnd',
'Expr_BinaryOp_Div',
'Expr_BinaryOp_Spaceship',
'Expr_BinaryOp_NotIdentical',
'Expr_BinaryOp_Mod',
'Expr_BinaryOp_NotEqual',
'Expr_BinaryOp_Greater',
'Expr_Isset',
'Expr_PostDec',
'Expr_List',
'Expr_FuncCall',
'Expr_NullsafeMethodCall',
'Expr_Error',
'Expr_BooleanNot',
'Expr_New',
'Expr_Clone',
'Expr_Yield',
'Expr_Cast_Array',
'Expr_Cast_Unset',
'Expr_Cast_Double',
'Expr_Cast_String',
'Expr_Cast_Int',
'Expr_Cast_Object',
'Expr_Cast_Bool',
'Expr_Variable',
'Expr_AssignRef',
'Expr_YieldFrom',
'Expr_NullsafePropertyFetch',
'Expr_AssignOp_Plus',
'Expr_AssignOp_Coalesce',
'Expr_AssignOp_BitwiseXor',
'Expr_AssignOp_Pow',
'Expr_AssignOp_BitwiseOr',
'Expr_AssignOp_Mul',
'Expr_AssignOp_Concat',
'Expr_AssignOp_ShiftRight',
'Expr_AssignOp_Minus',
'Expr_AssignOp_ShiftLeft',
'Expr_AssignOp_BitwiseAnd',
'Expr_AssignOp_Div',
'Expr_AssignOp_Mod',
'Expr_ClosureUse',
'Expr_PreInc',
'Expr_ArrayDimFetch',
'Expr_ArrowFunction',
'Expr_ShellExec',
'Expr_Include',
'Expr_BitwiseNot',
'Expr_Empty',
'Expr_StaticCall',
'Expr_ArrayItem',
'Expr_Print',
'Expr_Match',
'Expr_Throw',
'Expr_PreDec',
'Expr_Instanceof',
'Expr_PostInc',
'Expr_ClassConstFetch',
'Expr_MethodCall',
'Expr_Eval',
'Expr_Exit',
'Expr_UnaryMinus',
'Expr_Ternary',
'Expr_PropertyFetch',
'Expr_Assign',
'Expr_ConstFetch',
'Expr_Closure',
'Expr_ErrorSuppress',
'Expr_StaticPropertyFetch',
'Arg',
'MatchArm',
    ]

PHP_NODE_MAP = {x: i for (i, x) in enumerate(PHP_NODE_LIST)}