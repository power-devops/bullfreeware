;; This is a better default info path
(setq Info-directory-list '("/usr/lib/xemacs/xemacs-packages/info/" "/opt/freeware/info"))

;; run functions from the /usr/lib/xemacs/xemacs-packages/lisp/site-start.d directory
;; Files in this directory ending with ".el" are run on startup

(let (list)
  (setq list (directory-files "/usr/lib/xemacs/xemacs-packages/lisp/site-start.d" t "\\.el$"))
  (while list
    (load-file (car list))
    (setq list (cdr list)))
  )

;; Use the rpm-spec-mode for spec files
(require 'rpm-spec-mode)
(setq auto-mode-alist
      (cons '("\\.spec$" . rpm-spec-mode) auto-mode-alist))
