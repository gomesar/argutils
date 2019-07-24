filetype plugin indent on

" Custom statusline
set statusline=%F%m%r%h%w\ \ \ \ \ [F:%{&ff},\ T:%Y,\ A:\%03.3b(\%02.2B)]\ (%l,\ %v)[%03p%%-%L]

" YAML stuff
autocmd FileType yaml setlocal ts=2 sts=2 sw=2 expandtab

" ##############################################################################
" Plug-in setups
" Enable IndentGuide
colorscheme default
let g:indent_guides_auto_colors = 0
hi IndentGuidesOdd  ctermbg=red
hi IndentGuidesEven ctermbg=yellow

" Color scheme for vimdiff
if &diff
    colorscheme evening
endif
" ##############################################################################
" Plug-in binds
" Map NERDTree
map <C-t> :NERDTreeToggle<CR>
" IndentGuides
map <C-i> :IndentGuidesToggle<CR>

" ##############################################################################
" Common remaps
" Enables typo :W save too
command! W :w

" Navigate by display lines
noremap j gj
noremap k gk

" Easy switch
nnoremap <c-h> <c-w>h
nnoremap <c-j> <c-w>j
nnoremap <c-k> <c-w>k
nnoremap <c-l> <c-w>l

" ##############################################################################
" Common configurations
" Search highlight On
set hlsearch
" Statusline active
set laststatus=2
" show existing tab with 4 spaces width
set tabstop=4
" when indenting with '>', use 4 spaces width
set shiftwidth=4
" On pressing tab, insert 4 spaces
set expandtab
" Window min
set winwidth=80
